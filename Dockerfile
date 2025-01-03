FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3-tk && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt