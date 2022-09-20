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

# conda installs
## install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH
## clustalo (optional)
RUN conda install -c bioconda clustalo
## iqtree (optional)
RUN conda install -c bioconda iqtree
## krona (optional)
RUN conda install -c bioconda krona

# BLAST install
# For the latest BLAST version see https://ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/
ARG BLAST_version='2.13.0'
RUN wget --quiet 'ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/ncbi-blast-'${BLAST_version}'+-x64-linux.tar.gz'
RUN tar zxvpf 'ncbi-blast-'${BLAST_version}'+-x64-linux.tar.gz'
ENV PATH=./ncbi-blast-${BLAST_version}+/bin:$PATH

# LARGEVIS install (optional)


# DiVE install (optional)


# dnabarcoder install
## Added via requirements.txt don't know if it works?

# pip installs
COPY requirements.txt $APP
RUN pip install --no-cache-dir -r requirements.txt

# copy source code to image
COPY . $APP
