FROM ml_base

RUN sudo apt-get update -yq && \
    sudo apt-get install -yq \
	build-essential \
    gcc \
    g++ \
    clang \
    cmake \
    software-properties-common \
    nasm \
    pkgconf \
    libx264-dev \
    libsdl2-dev \
	>/dev/null && \
	sudo apt-get clean

WORKDIR /app

# CUDA
# RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin
# RUN mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
# RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
# RUN add-apt-repository "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/ /"
# RUN apt-get update && apt-get -yq install \
#     cuda-compiler-10-2 \
#     cuda-libraries-10-2 \
#     cuda-libraries-dev-10-2 \
#     cuda-compat-10-2 \
#     >/dev/null

# RUN git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git
# RUN cd /root/nv-codec-headers && git checkout n9.1.23.1

RUN git clone https://git.ffmpeg.org/ffmpeg.git
RUN cd /app/ffmpeg && git checkout n4.2.3

# ENV PATH="/usr/local/cuda-10.2/bin:$PATH"

COPY ./compile.sh /app/compile.sh
RUN /app/compile.sh

# RUN rm -rf /app/ffmpeg 
# RUN rm -rf /root/nv-codec-headers

RUN pip install clize
RUN pip install IPython

ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility,video,graphics
