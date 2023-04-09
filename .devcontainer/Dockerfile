FROM mcr.microsoft.com/vscode/devcontainers/python:3.7

LABEL maintainer="Nils Grote <nils.grote@smail.th-koeln.de>"
LABEL description="Fonduer Devcontainer"


RUN apt update && apt install -y libxml2-dev libxslt-dev python3-dev libpq-dev
RUN apt install -y poppler-utils
RUN apt install -y libmagickwand-dev
RUN apt install -y postgresql

RUN pip install --upgrade pip && pip install \
    matplotlib \
    ipywidgets \
    jupyter \
    fonduer \
 && python -m spacy download en