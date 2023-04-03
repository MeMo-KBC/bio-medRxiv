FROM hiromuhota/fonduer

LABEL maintainer="Nils Grote <nils.grote@smail.th-koeln.de>"
LABEL description="Fonduer Devcontainer"

USER root

RUN pip install --upgrade pip \
 && pip install \
    matplotlib \ 
 && python -m spacy download en


