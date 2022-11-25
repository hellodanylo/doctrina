ARG DOCTRINA_REPO=doctrina
FROM $DOCTRINA_REPO:base-latest

RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get update >/dev/null 2>&1 && \
    apt-get -yq install openjdk-11-jre-headless >/dev/null 2>&1

ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE ./conda.yml
RUN conda env create -n pyspark -f conda.yml

WORKDIR /app

RUN conda init zsh
RUN conda shell.zsh activate pyspark >>/root/.zshenv

