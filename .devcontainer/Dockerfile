FROM mcr.microsoft.com/vscode/devcontainers/python:3.7

LABEL maintainer="Nils Grote <nils.grote@smail.th-koeln.de>"
LABEL description="Fonduer Devcontainer"

RUN apt update && \
    apt install -y libxml2-dev \
    libxslt-dev \
    python3-dev \
    libpq-dev \
    curl \
    zsh \
    poppler-utils \
    libmagickwand-dev \
    postgresql


ENV HOME /home/$USER
USER $USER
ENV SHELL /bin/zsh

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

RUN pip install --upgrade pip && pip install \
    matplotlib \
    ipywidgets \
    jupyter \
    fonduer \
 && python -m spacy download en

