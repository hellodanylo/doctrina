#!/usr/bin/env bash

#cd /root/nv-codec-headers
#make install

cd /app/ffmpeg
./configure \
  --enable-gpl \
  --enable-nonfree \
  --enable-libx264 \
  --enable-ffplay \
  --extra-cflags=-I/usr/local/cuda-10.2/include \
  --extra-ldflags=-L/usr/local/cuda-10.2/lib64


  # --enable-cuda-nvcc \
  # --enable-cuvid \
  # --enable-nvenc \
  # --enable-libnpp \
 

make -j 10 install
make clean
