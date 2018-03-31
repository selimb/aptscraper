FROM arm32v6/python:alpine3.6

RUN mkdir -p /app
WORKDIR /app

COPY src /app/src
COPY setup.py /app/setup.py

RUN python setup.py install

VOLUME /work
WORKDIR /work

