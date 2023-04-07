FROM python:3.8.13-bullseye

ENV PYTHONBUFFERED=1

WORKDIR /backend

COPY requirements.txt ./

RUN ls

RUN pwd

RUN apt-get -y update

RUN apt-get -y upgrade

RUN apt-get install -y ffmpeg

RUN pip install -r ./requirements.txt

COPY . ./

EXPOSE 8000