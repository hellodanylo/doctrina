ARG DOCTRINA_REPO=doctrina
FROM $DOCTRINA_REPO:base-latest

ARG CONDA_ENV=mlflow
ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE $CONDA_PATH/conda_$CONDA_ENV.yml
RUN conda env create -n $CONDA_ENV -f $CONDA_PATH/conda_$CONDA_ENV.yml

WORKDIR /app
ENV PATH="$CONDA_PATH/envs/$CONDA_ENV/bin:$PATH"
