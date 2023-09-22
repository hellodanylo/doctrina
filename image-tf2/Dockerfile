ARG DOCTRINA_REPO=doctrina
FROM $DOCTRINA_REPO:base-latest

# conda-forge does not have tensorflow for cuda>11.2 at the moment
# https://anaconda.org/conda-forge/tensorflow/files
ENV CONDA_OVERRIDE_CUDA="11.2"
ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE $CONDA_PATH/conda_tf2.yml
RUN conda env create -n tf2 -f $CONDA_PATH/conda_tf2.yml

# Nvidia Runtime
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics

WORKDIR /app
ENV PATH="$CONDA_PATH/envs/tf2/bin:$PATH"
