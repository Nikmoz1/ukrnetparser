FROM python:3.6-alpine

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

COPY . /queue
WORKDIR /queue

RUN apk update && apk add postgresql-dev gcc libc-dev g++ python3-dev musl-dev libffi-dev
RUN apk add build-base

RUN pip3 install -r requirements.txt

# production
ENTRYPOINT celery -A tasks worker --loglevel=info