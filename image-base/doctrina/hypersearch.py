import os
from collections import OrderedDict

import pandas as pd

from doctrina.task import load_task, get_job_path


def find_experiments(workspace: str, job_name: str) -> dict:

    job_space = get_job_path(workspace, job_name)
    job_ids = os.listdir(job_space)

    workdirs = [job_space + '/' + job_id for job_id in job_ids]
    tasks = [load_task(workdir) for workdir in workdirs]

    experiments = {}
    for workdir, task in zip(workdirs, tasks):
        if 'experiment' not in task:
            continue
        if not os.path.exists(f'{workdir}/closing.time'):
            continue

        experiment = task['experiment']
        if experiment not in experiments:
            experiments[experiment] = []
        experiments[experiment].append(task)

    return experiments


def summarize_task_property(tasks: list, path: list) -> object:
    has_summary = False
    summary = None

    for task in tasks:
        has_value = True
        current = task

        for step in path:
            if step not in current:
                has_value = False
                break
            current = current[step]

        if has_value:
            if not has_summary:
                summary = current
                has_summary = True
            elif summary != current:
                summary = 'Varies'

    return summary


def summarize_experiments(experiments: dict, properties: list):
    experiments = OrderedDict(experiments)

    experiments_report = pd.DataFrame()
    experiments_report['name'] = [name for name, tasks in experiments.items()]
    experiments_report['tasks'] = [len(tasks) for name, tasks in experiments.items()]

    for prop in properties:
        experiments_report[prop[-1]] = [
            summarize_task_property(tasks, prop)
            for name, tasks in experiments.items()
        ]

    experiments_report = experiments_report.sort_values('name').reset_index(drop=True)
    return experiments_report
