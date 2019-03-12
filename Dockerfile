FROM python:3.6.5-slim-stretch
MAINTAINER Damian Myerscough

RUN mkdir -p /webapp/miruoncall && \
    mkdir -p /webapp/requirements && \
    mkdir -p /webapp/run && \
    mkdir -p /webapp/logs

COPY miruoncall /webapp/miruoncall/
COPY requirements/base.txt /webapp/requirements/
COPY entrypoint.sh /webapp/

RUN pip3 --no-cache-dir install -r /webapp/requirements/base.txt

WORKDIR /webapp/miruoncall

CMD ["/bin/bash", "/webapp/entrypoint.sh"]
