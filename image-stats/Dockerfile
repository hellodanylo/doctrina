ARG DOCTRINA_REPO=doctrina
FROM $DOCTRINA_REPO:base-latest

ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE $CONDA_PATH/conda_stats.yml
RUN conda env create -n stats -f $CONDA_PATH/conda_stats.yml

WORKDIR /app
ENV PATH="$CONDA_PATH/envs/stats/bin:$PATH"
