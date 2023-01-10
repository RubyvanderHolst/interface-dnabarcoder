# syntax=docker/dockerfile:1
###########
# BUILDER #
###########

# pull base image
FROM python:3.10 as builder

# set work directory
WORKDIR /usr/src/app

# prevents python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# keeps python from buffering stdin/stdout
ENV PYTHONUNBUFFERED=1

# pip installs
COPY interface-dnabarcoder/requirements.txt $APP
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

# pull base image
FROM python:3.10

# Update packages and install NCBI
# Downloads version 2.11.0 (two version behind newest) (on 14-11-22)
# (wget download doesn't save after build)
RUN apt-get update && apt-get install -y ncbi-blast+

# create app user
RUN useradd --create-home --shell /bin/bash app

# create environments
ENV HOME /home
ENV APP /home/app
ENV TOOL /home/tool

# set working directory
#RUN mkdir $APP
RUN mkdir $TOOL
WORKDIR $APP

# pip installs
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy interface code to image
COPY interface-dnabarcoder $APP

# copy dnabarcoder (necessary) code to image
COPY ./dnabarcoder.py $TOOL
COPY ./classification $TOOL/classification
COPY ./prediction $TOOL/prediction

# chown all the file to the app user
RUN chown -R app:app $HOME

USER app

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
