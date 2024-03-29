FROM python:3.7.8-slim

COPY requirements.txt requirements.txt
RUN pip install -U pip && pip install -r requirements.txt

COPY ./api /app/api
COPY ./bin /app/bin
COPY ./database /app/database
COPY wsgi.py /app/wsgi.py
WORKDIR /app

EXPOSE 8080

ENTRYPOINT ["bash", "/app/bin/run.sh"]
