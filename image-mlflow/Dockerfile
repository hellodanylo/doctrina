ARG DOCTRINA_REPO=doctrina
FROM $DOCTRINA_REPO:base-latest

ARG CONDA_ENV=mlflow
ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE ./conda.yml
RUN conda env create -n $CONDA_ENV -f ./conda.yml

WORKDIR /app
RUN sudo zsh -c "echo conda activate mlflow >>~/.zshenv"
