#!/usr/bin/env zsh

project_path=${0:a:h:h}

mkdir -p $project_path/local

python3 -m virtualenv $project_path/local/venv

$project_path/local/venv/bin/pip install -r $project_path/dev/requirements.txt
