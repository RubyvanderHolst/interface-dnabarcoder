# syntax=docker/dockerfile:1
# REMOVE PACKAGES WHEN NOT NECESSARY!!!

# pull base image
FROM python:3.10

# prevents python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# keeps python from buffering stdin/stdout
ENV PYTHONUNBUFFERED=1

# create environments
ENV HOME /home
ENV APP /home/app

# set working directory
RUN mkdir $APP
WORKDIR $APP

RUN apt-get update

# conda installs
# install miniconda
#ENV CONDA_DIR /opt/conda
#RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
#     /bin/bash ~/miniconda.sh -b -p /opt/conda
#ENV PATH=$CONDA_DIR/bin:$PATH
### clustalo (optional)
#RUN conda install -c bioconda clustalo
### iqtree (optional)
#RUN conda install -c bioconda iqtree
### krona (optional)
#RUN conda install -c bioconda krona

# pip installs
COPY requirements.txt $APP
RUN pip install --no-cache-dir -r requirements.txt

# BLAST install
# For the latest BLAST version see https://ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/
#ARG BLAST_version='2.13.0'
#RUN wget --quiet 'ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/ncbi-blast-'${BLAST_version}'+-x64-linux.tar.gz'
#RUN tar zxvpf 'ncbi-blast-'${BLAST_version}'+-x64-linux.tar.gz'
#RUN rm 'ncbi-blast-'${BLAST_version}'+-x64-linux.tar.gz'
#ENV PATH=./ncbi-blast-${BLAST_version}+/bin:$PATH

# Downloads version 2.11.0 (two version behind newest)
# (wget download doesn't save after build)
RUN apt-get install -y ncbi-blast+
RUN blastn -h

## install gsl (for LARGEVIS, so optional)
#RUN apt-get install -y libgsl-dev
## LARGEVIS install (optional)
#RUN git clone https://github.com/rugantio/LargeVis-python3.git && \
#    cd LargeVis-python3/Linux/ && \
#    g++ LargeVis.cpp main.cpp -o LargeVis -lm -pthread -lgsl -lgslcblas -Ofast -march=native -ffast-math && \
#    python setup.py install

## install node.js and nvm (for DiVE, so optional)
#ENV NODE_VERSION=16.17.0
#RUN apt install -y curl
#RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
#ENV NVM_DIR=${HOME}/.nvm
#RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
#RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
#RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
#ENV PATH="${HOME}/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
#RUN npm install -g npm
## DiVE install (optional)
#RUN git clone https://github.com/NLeSC/DiVE.git && \
#    cd DiVE && \
#    npm install connect serve-static

# dnabarcoder install
#RUN git clone https://github.com/vuthuyduong/dnabarcoder.git

# copy source code to image
COPY . $APP
