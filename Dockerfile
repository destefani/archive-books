# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

COPY . /workspace

WORKDIR /workspace

RUN apt-get update && apt-get install make && apt-get install -y python3-opencv
RUN pip3 install -r requirements.txt