FROM python:3.9.6-slim

RUN mkdir /coding_challenge/
COPY ./requirements.txt /coding_challenge/
COPY ./pytest.ini /coding_challenge/pytest.ini

RUN pip install --upgrade pip

RUN pip3 install -r /coding_challenge/requirements.txt

WORKDIR /coding_challenge/

ENV PYTHONDONTWRITEBYTECODE=true