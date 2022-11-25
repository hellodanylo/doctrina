#!/usr/bin/env zsh

set +x
set +e

build_dir=$1

git clone -b 3.0.0 https://github.com/Syllo/nvtop $build_dir

mkdir -p $build_dir/build
cd $build_dir/build

cmake -D AMDGPU_SUPPORT=off -D INTEL_SUPPORT=off ..
make
sudo make install