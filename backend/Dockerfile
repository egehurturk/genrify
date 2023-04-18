FROM python:3.8.13-bullseye

ENV PYTHONBUFFERED=1

WORKDIR /backend

COPY requirements.txt ./

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r ./requirements.txt

COPY . ./

RUN apt-get -y update

RUN apt-get -y upgrade

RUN apt-get install -y ffmpeg

EXPOSE 8000