FROM public.ecr.aws/ubuntu/ubuntu:22.04_stable AS base

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_PRIORITY=high

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install \
    # UI Requirements
    xvfb \
    x11vnc \
    curl \
    net-tools \
    software-properties-common \
    curl \
    vim \
    # Computer use might install additional tools using sudo
    sudo 
    
RUN apt-get install -y \
    libxcb-randr0-dev libxcb-xtest0-dev libxcb-xinerama0-dev libxcb-shape0-dev libxcb-xkb-dev \
    # For xvfb screen recording
    ffmpeg

RUN apt-get install -y \
    python3-pip \
    # for tkinter on Linux to use MouseInf
    python3-tk \
    python3-dev \
    gnome-screenshot 

# RUN apt-get -y --no-install-recommends install chromium-browser

RUN add-apt-repository ppa:mozillateam/ppa && \
    apt-get install -y --no-install-recommends \
    tint2 \
    firefox-esr \
    libreoffice \
    x11-apps \
    gedit \
    xpaint \
    galculator \
    unzip \
    xpdf && \
    apt-get clean

FROM base

ENV USERNAME=computeruse
ENV HOME=/home/$USERNAME
RUN useradd -m -s /bin/bash -d $HOME $USERNAME
RUN echo "${USERNAME} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER computeruse
WORKDIR $HOME

COPY --chown=$USERNAME:$USERNAME app/requirements.txt $HOME/app/requirements.txt
RUN python3.10 -m pip install -r $HOME/app/requirements.txt

COPY --chown=$USERNAME:$USERNAME app $HOME/app/

COPY --chown=$USERNAME:$USERNAME entrypoint.sh $HOME/
RUN chmod +rx $HOME/entrypoint.sh

ARG DISPLAY_NUM=0
ARG HEIGHT=768
ARG WIDTH=1024
ENV DISPLAY_NUM=$DISPLAY_NUM
ENV HEIGHT=$HEIGHT
ENV WIDTH=$WIDTH

ENV LOG_OUTPUT_FOLDER=${HOME}/logs
RUN mkdir -p ${LOG_OUTPUT_FOLDER}

#x11vnc port
EXPOSE 5900 
ENTRYPOINT [ "./entrypoint.sh" ]
