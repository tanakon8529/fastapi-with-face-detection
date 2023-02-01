# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
FROM python:3.9-slim-bullseye

# set environment variables
ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# set working directory
WORKDIR ./code

# copy dependencies and update pip
COPY requirements.txt .
RUN python -m pip install --upgrade pip

# install dependencies
RUN pip install -r requirements.txt

# copy project
COPY . /code/
