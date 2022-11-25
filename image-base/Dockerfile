FROM ghcr.io/hellodanylo/humus:main

ENV DEBIAN_FRONTEND="noninteractive"
ENV TZ="America/Los_Angeles"

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
USER $user_name:$group_name

WORKDIR /app
RUN sudo chown -R $user_name:$group_name /app

ARG CONDA_REPO=https://repo.anaconda.com/miniconda
ARG CONDA_INSTALLER=Miniconda3-py39_4.10.3-Linux-x86_64.sh
RUN wget -q $CONDA_REPO/$CONDA_INSTALLER
RUN bash $CONDA_INSTALLER -q -b -p /app/miniconda && rm -rf $CONDA_INSTALLER

# Non-interactive zsh will have access to miniconda.
ENV PATH="/app/miniconda/bin:$PATH"

# Interactive zsh gets the rest of the miniconda setup.
RUN /app/miniconda/bin/conda init zsh

ARG CONDA_RC=condarc_default.yml
COPY $CONDA_RC /home/${user_name}/.condarc

COPY nvtop_install.sh ./
RUN mkdir -p /app/nvtop && \
    /app/nvtop_install.sh /app/nvtop && \
    rm -rf /app/nvtop*
