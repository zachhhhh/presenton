FROM python:3.11-slim
WORKDIR /app/servers/fastapi
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libmagic1 \
    git \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade pip
COPY servers/fastapi /app/servers/fastapi
RUN pip install --no-cache-dir -e .
RUN mkdir -p /app/data
ENV APP_DATA_DIRECTORY=/app/data
ENV USER_CONFIG_PATH=/app/data/user_config.json
ENV TEMP_DIRECTORY=/tmp
ENV CAN_CHANGE_KEYS=true
EXPOSE 10000
CMD ["sh","-c","uvicorn api.main:app --host 0.0.0.0 --port ${PORT}"]
