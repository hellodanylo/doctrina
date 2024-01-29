ARG DOCTRINA_REPO=doctrina
FROM $DOCTRINA_REPO:base-latest

ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE /app/conda/conda_torch.yml

#ENV CONDA_OVERRIDE_CUDA="11.8"
RUN conda env create -n torch -f /app/conda/conda_torch.yml

WORKDIR /app
ENV PATH="/app/conda/envs/torch/bin:$PATH"
