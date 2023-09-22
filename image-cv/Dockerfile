ARG DOCTRINA_REPO=doctrina
FROM $DOCTRINA_REPO:base-latest

ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE $CONDA_PATH/conda_cv.yml
RUN conda env create -n cv -f $CONDA_PATH/conda_cv.yml

ENV PATH="$CONDA_PATH/envs/cv/bin:$PATH"
