FROM python:3.12.2-slim
RUN apt-get update
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p main
COPY main main
RUN mkdir -p web_client
COPY web_client web_client
COPY manage.py .
COPY gunicorn.py .
WORKDIR /app/main/image
RUN mkdir uploaded
WORKDIR /app
RUN python manage.py migrate
RUN mkdir static
RUN python manage.py collectstatic
