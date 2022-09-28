# pull official base image
FROM python:3.9.6-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

#need to install these for dependencies
RUN apt-get update && apt-get -y install libpq-dev gcc
RUN apt-get install -y build-essential libssl-dev libffi-dev
RUN apt-get install -y gdal-bin libgdal-dev
RUN apt-get install -y python3-gdal
RUN apt-get install -y binutils libproj-dev

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
