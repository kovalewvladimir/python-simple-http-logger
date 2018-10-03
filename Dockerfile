FROM python:3.7-slim

LABEL Name=python-simple-http-logger Version=0.0.1
EXPOSE 9000

WORKDIR /app
ADD . /app
RUN mkdir logs

CMD ["python3", "server.py"]