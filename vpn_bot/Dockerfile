FROM python:3.10.6-slim

RUN mkdir /tg_bot

COPY ./requirements.txt /tg_bot

RUN pip install -r /tg_bot/requirements.txt --no-cache-dir

COPY . /tg_bot

WORKDIR /tg_bot

CMD python3 start.py