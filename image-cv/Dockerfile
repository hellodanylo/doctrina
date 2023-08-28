ARG DOCTRINA_REPO=doctrina
FROM $DOCTRINA_REPO:base-latest

ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE ./conda.yml
RUN conda env create -n cv -f conda.yml

ENV PATH="/app/miniconda/envs/cv/bin:$PATH"
