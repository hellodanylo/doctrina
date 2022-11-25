ARG DOCTRINA_REPO=doctrina
FROM $DOCTRINA_REPO:base-latest

ENV CONDA_OVERRIDE_CUDA="11.2"
ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE ./conda.yml
RUN conda env create -n tf2 -f conda.yml

# Nvidia Runtime
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics

WORKDIR /app
ENV PATH="/app/miniconda/envs/torch/bin:$PATH"