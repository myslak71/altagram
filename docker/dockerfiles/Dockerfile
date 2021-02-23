FROM python:3.9.1-slim-buster

WORKDIR /code

COPY requirements.txt /code/
RUN pip3 install  -r requirements.txt

COPY . /code
RUN pip3 install .
