ARG DOCTRINA_REPO=doctrina
FROM $DOCTRINA_REPO:base-latest

ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE ./conda.yml

ENV CONDA_OVERRIDE_CUDA="11.2"
RUN conda env create -n torch -f conda.yml

WORKDIR /app
ENV PATH="/app/miniconda/envs/torch/bin:$PATH"
