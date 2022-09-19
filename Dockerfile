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
## clustalo
RUN conda install -c bioconda clustalo
## iqtree
RUN conda install -c bioconda iqtree
## krona
RUN conda install -c bioconda krona

# BLAST install

# LARGEVIS install

# DiVE install

# pip installs
COPY requirements.txt $APP
RUN pip install --no-cache-dir -r requirements.txt

# copy source code to image
COPY . $APP
