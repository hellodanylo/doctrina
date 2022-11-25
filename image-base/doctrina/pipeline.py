import json

from joblib import Parallel, delayed

from doctrina.task import execute


def load_runtime(workdir):
    with open(f'{workdir}/runtime.json', 'r') as f:
        return json.loads(f.read())


def save_runtime(workdir, runtime):
    with open(f'{workdir}/runtime.json', 'w') as f:
        return f.write(json.dumps(runtime, indent=True))


def execute_pipeline(task: dict):
    workdir = task['workdir']
    stages = task['stages']

    if 'resume' in task:
        runtime = load_runtime(task['resume'])
        save_runtime(workdir, runtime)
    else:
        runtime = {}

    for stage in stages:
        if stage in runtime:
            print(f'Stage {stage} restored from runtime')
            continue

        stage_task = stages[stage]

        try:
            if type(stage_task) == list:
                concurrent_jobs = task['parallel_processes']

                for t in stage_task:
                    t['upstream'] = runtime.copy()

                # Sub-processes update the task with
                # job and workdir information, which this pipeline
                # needs to capture so that the runtime object is complete.
                stage_task = Parallel(n_jobs=concurrent_jobs, verbose=10)([
                    delayed(execute)(t) for t in stage_task
                ])

                for t in stage_task:
                    del t['upstream']
            else:
                stage_task['upstream'] = runtime.copy()
                execute(stage_task)
                del stage_task['upstream']

        except Exception as e:
            print(f'Stage {stage} failed, resume from {workdir}')
            raise e

        runtime[stage] = stage_task

        save_runtime(task['workdir'], runtime)

    print(f'Finished pipeline {workdir}')