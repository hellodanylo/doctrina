ARG DOCTRINA_REPO=doctrina
FROM $DOCTRINA_REPO:base-latest

ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE ./conda.yml
RUN conda env create -n xgb -f conda.yml

WORKDIR /app
RUN sudo zsh -c "echo conda activate xgb >>~/.zshenv"
