#!/usr/bin/env bash

set -e

image="ml_ffmpeg"
container="ml-ffmpeg"

docker build -t $image .
