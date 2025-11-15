FROM python:3.11-slim-bookworm

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set writable defaults for runtime
ENV APP_DATA_DIRECTORY=/tmp/app_data
ENV TEMP_DIRECTORY=/tmp

WORKDIR /app/servers/fastapi

# System dependencies for building optional wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libpng-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy repository (Dockerfile path is servers/fastapi)
COPY . /app/

# Install Python dependencies
RUN pip install -U pip setuptools wheel && \
    pip install --extra-index-url https://download.pytorch.org/whl/cpu --prefer-binary --no-cache-dir .

EXPOSE 8000

# Default command (respect Render-provided PORT if set)
CMD ["sh", "-lc", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
