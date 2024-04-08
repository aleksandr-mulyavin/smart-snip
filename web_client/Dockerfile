FROM python:3.12.2-slim

RUN apt-get update

WORKDIR /app
RUN mkdir main web_client static

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY main main
COPY web_client web_client
COPY manage.py .
COPY gunicorn.py .

WORKDIR /app/main/image
RUN mkdir uploaded

WORKDIR /app
RUN python manage.py migrate \
    && python manage.py collectstatic
