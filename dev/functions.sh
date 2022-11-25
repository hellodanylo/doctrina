#!/usr/bin/env zsh

dev_path="${0:a:h}"

PATH="$dev_path/../local/venv/bin:$PATH"

# General
alias c="$dev_path/cli.py"

# Docker
alias d='docker'
alias dc='docker-compose'