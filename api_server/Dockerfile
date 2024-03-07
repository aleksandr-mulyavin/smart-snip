FROM python:3.12.2-slim
RUN apt-get update && apt-get install -y --force-yes tesseract-ocr
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p domain
COPY src/domain domain
RUN mkdir -p service
COPY src/service service
COPY src/main.py .
COPY secrets.txt .
COPY settings.yaml .
RUN mkdir logs
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]