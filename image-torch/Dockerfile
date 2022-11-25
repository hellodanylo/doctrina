FROM ml_base

ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE ./conda.yml

ENV CONDA_OVERRIDE_CUDA="11.2"
RUN conda env create -n torch -f conda.yml

WORKDIR /app
RUN sudo zsh -c "echo conda activate torch >>~/.zshenv"