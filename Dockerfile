# Python slim base
FROM python:3.12-slim AS base
# Set working directory
WORKDIR /var/www/tunedgpt
# Copy over requirements first (Leverages Docker Cache?)
COPY requirements.txt .
# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Artifact to start configuring the venv
FROM base AS artifact
# Install Python dependencies globally (no venv)
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
# Copy the rest of the app
COPY . .

# Production image
FROM artifact AS prod
# Start Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "--reload", "app:create_app()"]

# Dev image
FROM artifact AS dev
# Start Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "app:create_app()"]
