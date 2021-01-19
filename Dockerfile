FROM python:3.9-slim-buster
RUN apt update && apt install gcc libpq-dev -y
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD ./academy/ /app/