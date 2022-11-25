FROM ml_base

ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE ./conda.yml
RUN conda env create -n cv -f conda.yml

WORKDIR /root
RUN sudo zsh -c "echo conda activate cv >>~/.zshenv"