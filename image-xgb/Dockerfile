ARG DOCTRINA_REPO=doctrina
FROM $DOCTRINA_REPO:base-latest

ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE $CONDA_PATH/conda_xgb.yml
RUN conda env create -n xgb -f $CONDA_PATH/conda_xgb.yml

WORKDIR /app
ENV PATH="$CONDA_PATH/envs/xgb/bin:$PATH"
