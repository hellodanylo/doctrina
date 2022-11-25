#!/usr/bin/env bash

set -e

image="doctrina-ffmpeg"

docker build -t $image .
