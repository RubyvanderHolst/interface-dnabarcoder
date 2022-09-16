# syntax=docker/dockerfile:1
# Add wheel if downloading takes long!

# pull base image
FROM python:3.10

# prevents python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# keeps python from buffering stdin/stdout
ENV PYTHONUNBUFFERED=1

# set work directory
RUN mkdir /app
WORKDIR /app

# install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/