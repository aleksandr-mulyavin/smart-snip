FROM python:3.12.2-slim
RUN apt-get update
RUN apt-get install -y --force-yes tesseract-ocr tesseract-ocr-rus
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p domain
COPY src/domain domain
RUN mkdir -p service
COPY src/service service
COPY src/*.py .
RUN mkdir logs
