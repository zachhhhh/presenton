FROM python:3.11-slim-bookworm

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set writable defaults for runtime
ENV APP_DATA_DIRECTORY=/tmp/app_data
ENV TEMP_DIRECTORY=/tmp

WORKDIR /app

# System dependencies (keep minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy FastAPI backend (the workflow sets context to servers/fastapi)
COPY . /app/

# Install Python dependencies
RUN pip install -U pip setuptools wheel && \
    pip install --extra-index-url https://download.pytorch.org/whl/cpu --prefer-binary --no-cache-dir -e .

EXPOSE 8000

# Default command (override with platform start command as needed)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
