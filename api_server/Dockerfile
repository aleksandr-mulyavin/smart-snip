FROM python:3.12.2-slim

RUN apt-get update \
    && apt-get install -y --force-yes tesseract-ocr tesseract-ocr-rus

WORKDIR /app
RUN mkdir domain service logs

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src/domain domain
COPY src/service service
COPY src/*.py .

COPY arial.ttf /usr/share/fonts/truetype/.
