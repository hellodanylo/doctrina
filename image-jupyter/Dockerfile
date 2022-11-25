FROM ml_tf2 as tf2
FROM ml_xgb as xgb
FROM ml_cv as cv
# FROM ml_pyspark as pyspark
FROM ml_stats as stats
FROM ml_torch as torch
FROM ml_base

# Required to run "conda activate"
SHELL ["zsh", "-i", "-c"]

# Conda environment
ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE ./conda.yml
RUN conda env create -n jupyter -f conda.yml

## Jupyter Extensions
RUN conda activate jupyter && \
    jupyter labextension install --no-build @jupyter-widgets/jupyterlab-manager \
    jupyter lab build \
    >/dev/null

COPY --from=tf2 /app/miniconda/envs/tf2 /app/miniconda/envs/tf2
RUN /app/miniconda/envs/tf2/bin/ipython kernel install --user --name=tf2

COPY --from=xgb /app/miniconda/envs/xgb /app/miniconda/envs/xgb
RUN /app/miniconda/envs/xgb/bin/ipython kernel install --user --name=xgb

COPY --from=cv /app/miniconda/envs/cv /app/miniconda/envs/cv
RUN /app/miniconda/envs/cv/bin/ipython kernel install --user --name=cv

# COPY --from=pyspark /app/miniconda/envs/pyspark /app/miniconda/envs/pyspark
# RUN /app/miniconda/envs/pyspark/bin/ipython kernel install --user --name=pyspark

COPY --from=stats /app/miniconda/envs/stats /app/miniconda/envs/stats
RUN /app/miniconda/envs/stats/bin/ipython kernel install --user --name=stats

COPY --from=torch /app/miniconda/envs/torch /app/miniconda/envs/torch
RUN /app/miniconda/envs/torch/bin/ipython kernel install --user --name=torch

# Spark kernel
# RUN export DEBIAN_FRONTEND=noninteractive
# RUN apt-get update >/dev/null 2>&1 && \
#     apt-get -yq install \
#         openjdk-11-jre-headless \
#         libgl1-mesa-glx \
#         libglu1-mesa-dev \
#         libxi6 \
#         >/dev/null 2>&1

# Nvidia Runtime
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics
ENV SHELL=/bin/zsh

CMD conda activate jupyter && \
    jupyter lab \
    --notebook-dir=/app \
    --ip='0.0.0.0' \
    --port=80 \
    --no-browser
