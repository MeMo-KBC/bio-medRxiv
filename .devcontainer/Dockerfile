FROM hiromuhota/fonduer

LABEL maintainer="Nils Grote <nils.grote@smail.th-koeln.de>"
LABEL description="Fonduer Devcontainer"

RUN apt-get update

RUN pip install --upgrade pip \
 && pip install \
    matplotlib \ 
 && python -m spacy download en


