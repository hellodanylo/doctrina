#!/usr/bin/env zsh

DEV_PATH="${0:a:h}"

# General
conda activate ml-dev
alias c="$DEV_PATH/cli.py"

# Docker
alias d='docker'
alias dc='docker-compose'
