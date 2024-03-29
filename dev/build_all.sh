#!/usr/bin/env zsh

dev_path="${0:a:h}"
source $dev_path/functions.sh

c docker-build base

c docker-build stats &
c docker-build tf2 &
c docker-build xgb &
c docker-build cv &
c docker-build ffmpeg &
c docker-build torch &
wait 

c docker-build jupyter
