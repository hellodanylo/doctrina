#!/usr/bin/env zsh

set -eux

# For some reason, cuDNN needs to be installed separately from CUDA.
apt-get install -yq \
    libcudnn8=8.6.0.163-1+cuda11.8 \
    libcudnn8-dev=8.6.0.163-1+cuda11.8

apt-get install -yq \
    libnvinfer8=8.6.0.12-1+cuda11.8 \
    libnvinfer-dev=8.6.0.12-1+cuda11.8 \
    libnvinfer-headers-dev=8.6.0.12-1+cuda11.8 \
    libnvinfer-plugin8=8.6.0.12-1+cuda11.8 \
    libnvparsers8=8.6.0.12-1+cuda11.8 \
    libnvinfer-vc-plugin8=8.6.0.12-1+cuda11.8 \
    libnvonnxparsers8=8.6.0.12-1+cuda11.8 \
    python3-libnvinfer=8.6.0.12-1+cuda11.8