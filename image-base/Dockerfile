ARG HUMUS_REPO=ghcr.io/hellodanylo/humus
FROM $HUMUS_REPO:main

ENV DEBIAN_FRONTEND="noninteractive"
ENV TZ="America/Los_Angeles"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime
RUN echo $TZ | tee -a /etc/timezone

RUN apt-get update -y && apt-get install -y \
    build-essential \
    fontconfig \
    libncurses5-dev \
    libncursesw5-dev \
    cmake \
    >/dev/null

ARG user_id=1000
ARG user_name=user
ARG group_id=1000
ARG group_name=user

RUN /opt/humus/create_user.sh $user_id $user_name $group_id $group_name
USER $user_name

WORKDIR /app
RUN sudo chown -R $user_name:$group_name /app

ENV CONDA_PATH=/app/conda
ARG CONDA_REPO=https://repo.anaconda.com/miniconda
ARG CONDA_INSTALLER=Miniconda3-py311_23.5.2-0-Linux-x86_64.sh
RUN wget -q $CONDA_REPO/$CONDA_INSTALLER
RUN bash $CONDA_INSTALLER -b -p $CONDA_PATH && rm -rf $CONDA_INSTALLER

# Non-interactive zsh will have access to miniconda.
ENV PATH="$CONDA_PATH/bin:$PATH"

# Interactive zsh gets the rest of the miniconda setup.
RUN conda init zsh

ARG CONDA_RC=condarc_default.yml
COPY $CONDA_RC /home/${user_name}/.condarc

COPY nvtop_install.sh ./
RUN mkdir -p /app/nvtop && \
    /app/nvtop_install.sh /app/nvtop && \
    rm -rf /app/nvtop*

# Required to run "conda activate"
SHELL ["zsh", "-i", "-c"]

# Conda environment
ARG CONDA_FILE=conda_lock.yml
COPY $CONDA_FILE $CONDA_PATH/conda_jupyter.yml
RUN conda env create -n jupyter -f $CONDA_PATH/conda_jupyter.yml

# Nvidia Runtime
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics
ENV SHELL=/bin/zsh

RUN mkdir -p /home/$user_name/.local/share

COPY install_cuda.sh /app/install_cuda.sh
COPY doctrina /app/doctrina

CMD conda activate jupyter && \
    jupyter lab \
    --notebook-dir=/app \
    --ip='0.0.0.0' \
    --port=80 \
    --no-browser
