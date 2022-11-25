FROM ml_jupyter as jupyter
FROM ml_base

COPY --from=jupyter /app/miniconda/envs/jupyter /app/miniconda/envs/jupyter
RUN /app/miniconda/envs/jupyter/bin/ipython kernel install --user --name=jupyter

RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get update >/dev/null 2>&1 && \
    apt-get -yq install openjdk-11-jre-headless >/dev/null 2>&1

ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE ./conda.yml
RUN conda env create -n pyspark -f conda.yml

WORKDIR /app

RUN conda init zsh
RUN conda shell.zsh activate pyspark >>/root/.zshenv

