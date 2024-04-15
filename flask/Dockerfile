# syntax=docker/dockerfile:1.4
FROM python:3.10-alpine AS deploy

WORKDIR /src
COPY requirements.txt /src
RUN  pip3 install -r requirements.txt

COPY . .

RUN adduser -D user
USER user

CMD ["python3", "server.py"]
