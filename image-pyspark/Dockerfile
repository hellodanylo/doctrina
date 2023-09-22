ARG DOCTRINA_REPO=doctrina
FROM $DOCTRINA_REPO:base-latest

RUN export DEBIAN_FRONTEND=noninteractive
RUN sudo apt-get update >/dev/null 2>&1 && \
    sudo apt-get -yq install openjdk-11-jre-headless >/dev/null 2>&1

ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE $CONDA_PATH/conda_pyspark.yml
RUN conda env create -n pyspark -f $CONDA_PATH/conda_pyspark.yml

WORKDIR /app
ENV PATH="$CONDA_PATH/envs/pyspark/bin:$PATH"
