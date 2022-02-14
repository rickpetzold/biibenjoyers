# syntax=docker/dockerfile:1

FROM ubuntu:18.04
SHELL [ "/bin/bash", "--login", "-c" ]
ARG username=bibbot
ARG uidd=1000
ARG gidd=100
ENV USER $username
ENV UID $uidd
ENV GID $gidd
ENV HOME /home/$USER

RUN adduser --force-badname $USER --disabled-password \
 --gecos "Non-root user" \
 --uid $UID \
 --gid $GID \
 --home $HOME 

USER $USER 

ENV MINICONDA_VERSION latest
ENV CONDA_DIR $HOME/miniconda3

USER root
RUN apt-get update \
 && apt-get install -y wget \
 && rm -rf /var/lib/apt/lists/*


RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-$MINICONDA_VERSION-Linux-x86_64.sh \
	-O ~/miniconda.sh && chmod +x ~/miniconda.sh && \
	~/miniconda.sh -b -p $CONDA_DIR && rm ~/miniconda.sh

ENV PATH=$CONDA_DIR/bin:$PATH
RUN echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.profile
RUN conda init bash

ENV PROJECT_DIR $HOME/bibbot
RUN mkdir $PROJECT_DIR
WORKDIR $PROJECT_DIR

ADD ./environment.yml ./environment.yml
ADD ./entrypoint.sh ./entrypoint.sh


ENV ENV_PREFIX $PWD/env
RUN conda update --name base --channel defaults conda && \
 conda env create --prefix $ENV_PREFIX --file \
./environment.yml --force && conda clean --all --yes

RUN apt update && apt-get install -y firefox firefox-locale-de && apt-get install tesseract-ocr -y && apt-get -y install xauth && apt-get -y install tzdata

# Timezone

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY . .

RUN chown $UID:$GID ./environment.yml
RUN chown $UID:$GID ./entrypoint.sh && \
	chmod u+x ./entrypoint.sh

USER $USER
ENTRYPOINT [ "./entrypoint.sh" ]


