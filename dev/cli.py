#!/usr/bin/env python3

import os
import subprocess
from typing import Optional

import clize

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def jupyter_up():
    subprocess.run([f"{project_path}/dev/start_jupyter.sh"])


def conda_init(image_name):
    env_name = f"ml-{image_name}-init"
    subprocess.run(["conda", "env", "remove", "-n", env_name])
    subprocess.run(
        [
            "conda",
            "env",
            "create",
            "-n",
            env_name,
            "-f",
            f"{project_path}/image-{image_name}/conda_init.yml",
        ],
        check=True,
    )
    proc = subprocess.run(
        ["conda", "env", "export", "-n", env_name], capture_output=True, check=True
    )
    with open(f"{project_path}/image-{image_name}/conda_lock.yml", "w") as f:
        f.write(proc.stdout.decode())


def conda_lock(image_name):
    proc = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "-it",
            f"ml_{image_name}",
            "conda",
            "env",
            "export",
            "-n", image_name
        ], capture_output=True, check=True
    )
    with open(f"{project_path}/image-{image_name}/conda_lock.yml", "w") as f:
        f.write(proc.stdout.decode())


def docker_build(
    *image_names: str, 
    conda_init: bool = False, 
    conda_cache: bool = False, 
    user_name: str = 'user', 
    group_name: str = 'user',
    network: Optional[str] = None
):
    for image_name in image_names:
        subprocess.run(
            [
                "docker",
                "build",
                *(['--build-arg', 'CONDA_FILE=conda_init.yml'] if conda_init else []),
                *(['--build-arg', 'CONDA_RC=condarc_cache.yml'] if conda_cache else []),
                '--build-arg', f'user_name={user_name}',
                '--build-arg', f'group_name={group_name}',
                *(["--network", network] if network is not None else []),
                "-t",
                f"ml_{image_name}",
                f"{project_path}/image-{image_name}",
            ],
            check=True
        )


if __name__ == "__main__":
    clize.run([
        jupyter_up,
        docker_build,
        conda_init,
        conda_lock
    ])
