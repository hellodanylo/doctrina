#!/usr/bin/env zsh

set -eux

cuda_version=11-8
cuda_version_dot=$(echo $cuda_version | tr - .)

# Other packages:
#    cuda-compiler-$cuda_version \
#    cuda-libraries-$cuda_version \
#    cuda-libraries-dev-$cuda_version \
#    cuda-compat-$cuda_version \
#    cuda-nvprof-$cuda_version \
#    cuda-cupti-$cuda_version \
#    cuda-nsight-compute-$cuda_version \
#    cuda-gdb-$cuda_version \
 
sudo wget -O /etc/apt/preferences.d/cuda-repository-pin-600 \
    https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin

sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub
sudo add-apt-repository "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/ /"
sudo apt-get update >/dev/null
sudo apt-get -yq install \
    cuda-nsight-compute-$cuda_version \
    >/dev/null

sudo ln -s /usr/local/cuda-$cuda_version_dot /usr/local/cuda
echo 'PATH=/usr/local/cuda/bin:$PATH' >>$HOME/.humus/zsh/zshenv
