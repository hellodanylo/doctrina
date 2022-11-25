import datetime as dt
import json
import os
import random

import boto3
import mlflow

from doctrina.tree import implode_tree


def encode(function):
    if '__wrapped_function__' in function.__dict__:
        function = function.__wrapped_function__

    return [function.__module__, function.__name__]


def execute(task):
    module_path = task['function'][0]
    module = __import__(module_path)

    steps = module_path.split('.')
    steps.append(task['function'][1])

    current = module
    for step in steps[1:]:
        current = getattr(current, step)

    task['job'] = task['function'][1]

    start_task(task)
    current(task)
    close_task(task)

    return task


def start_task(task):
    workspace = task['workspace']
    job = task['job']

    workspace_job = get_job_path(workspace, job)

    if not os.path.exists(workspace_job):
        os.makedirs(workspace_job)

    timestamp = dt.datetime.now().strftime('%Y%m%d-%H%M%S')
    noise = '{0:x}'.format(random.randint(0,2**128))
    new_job_tag = f'{timestamp}_{noise}'
    workdir = f'{workspace_job}/{new_job_tag}'

    task['workdir'] = workdir

    print(f'Workdir: {workdir}')
    # print(json.dumps(task, indent=True))

    os.mkdir(workdir)
    save_task(workdir, task)
    save_workdir_to_private_s3(workdir)

    return workdir


def close_task(task):

    workdir = task['workdir']
    with open(f'{workdir}/closing.time', 'w') as f:
        f.write(dt.datetime.now().isoformat())

    save_workdir_to_private_s3(task['workdir'])


def save_workdir_to_private_s3(workdir):
    bucket = os.environ['APP_S3_BUCKET_PRIVATE']
    if bucket == '':
        print('Skipping S3 upload due to missing bucket')
        return

    code = os.system(f'aws s3 sync {workdir} s3://{bucket}{workdir}')

    if code != 0:
        raise Exception('Failed to save the workdir to S3')


def get_last_workdir(workspace: str, job: str):
    workspace_job = get_job_path(workspace, job)

    past_job_ids = os.listdir(workspace_job)
    last_job_id = sorted(past_job_ids)[-1]

    return f'{workspace_job}/{last_job_id}'


def load_task(workdir):
    with open(f'{workdir}/task.json', 'r') as f:
        return json.loads(f.read())


def save_task(workdir, task):
    # Saving the hyperparams
    with open(f'{workdir}/task.json', 'w') as f:
        f.write(json.dumps(task, indent=True))


def is_task_tagged(task, tag_key, tag_value):
    if 'tags' not in task:
        return False

    if tag_key not in task['tags']:
        return False

    return task['tags'][tag_key] == tag_value


def find_tasks_by_tag(workspace, job_name, tag_key, tag_value):

    jobspace = get_job_path(workspace, job_name)
    workdirs = [f'{jobspace}/{w}' for w in os.listdir(jobspace)]

    all_tasks = {w: load_task(w) for w in workdirs}
    matching_tasks = {
        w: t for w, t in all_tasks.items()
        if is_task_tagged(t, tag_key, tag_value)
    }

    return matching_tasks


def get_storage_path():
    return os.environ['APP_STORAGE_PATH']


def get_job_path(workspace, job):
    return f'{get_storage_path()}/{workspace}/jobs/{job}'


def get_task_workdir(workspace, job, task_id):
    return f'{get_job_path(workspace, job)}/{task_id}'


def is_task_finished(workspace, job, task_id):
    return os.path.exists(f'{get_last_workdir(workspace, job, task_id)}/closing.time')


def find_incomplete_tasks(workspace):
    functions = os.listdir(f'{get_storage_path()}/{workspace}/jobs')

    tasks = []
    for name in functions:
        tasks += [
            f'{get_storage_path()}/{workspace}/jobs/{name}/{task_id}'
            for task_id in os.listdir(f'{get_storage_path()}/{workspace}/jobs/{name}')
        ]

    incomplete_tasks = [
        task for task in tasks
        if not os.path.exists(f'{task}/closing.time')
    ]

    return incomplete_tasks


def remove_workdirs(workdirs):
    for workdir in workdirs:
        print(f'Removing {workdir}')
        os.system(f'rm -rf {workdir}')

        s3 = boto3.resource('s3')
        bucket = s3.Bucket(os.environ['APP_S3_BUCKET_PRIVATE'])

        for obj in bucket.objects.all():
            if obj.key.startswith(workdir[1:]):
                obj.delete()


def clean_workspace(workspace):
    """
    :param workspace:
    """
    remove_workdirs(find_incomplete_tasks(workspace))


def mlflow_run(task_function):
    def wrapper(task: dict):
        experiment = mlflow.get_experiment_by_name(task['experiment'])
        if experiment is None:
            experiment_id = mlflow.create_experiment(task['experiment'])
        else:
            experiment_id = experiment.experiment_id

        with mlflow.start_run(experiment_id=experiment_id):
            mlflow.log_params(implode_tree(task, separator='/'))
            task_function(task)
            mlflow.log_artifacts(task['workdir'])

    wrapper.__wrapped_function__ = task_function
    return wrapper