#!/usr/bin/env bash

xhost +

docker run \
    --rm \
	--gpus all \
	-h ml-ffmpeg \
	-v "$PWD:/app/source" \
    -v /mnt:/mnt \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
	-w /app/source \
    -e DISPLAY \
	-it ml_ffmpeg \
    $*
