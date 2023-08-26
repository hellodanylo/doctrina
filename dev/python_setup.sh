#!/usr/bin/env zsh
set -uex

project_path=${0:a:h:h}

mkdir -p $project_path/local

python3 -m venv $project_path/local/venv

$project_path/local/venv/bin/pip install -r $project_path/dev/requirements.txt
