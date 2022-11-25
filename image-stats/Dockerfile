FROM ml_base

ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE ./conda.yml
RUN conda env create -n stats -f conda.yml

WORKDIR /app
RUN sudo zsh -c "echo conda activate stats >>~/.zshenv"