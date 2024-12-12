# Base image
FROM python:3.10.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    libpcre3-dev \
    libpq-dev \
    libmagic1 \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies management tool (uv)
RUN pip install uv

# Copy pyproject.toml and install dependencies using uv
COPY pyproject.toml .
RUN uv venv && \
    uv pip install --system .

## Copy the init.sh script and make it executable
COPY ./docker/fastapi/init.sh .
RUN chmod +x ./init.sh

# Copy the rest of the application code
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Set ENTRYPOINT to the init.sh script
ENTRYPOINT ["/bin/bash", "./docker/fastapi/init.sh"]
#CMD ["python", "main.py"]