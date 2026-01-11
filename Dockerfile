# Python slim base
FROM python:3.12-slim AS base
# Set working directory
WORKDIR /var/www/tunedgpt
# Copy over requirements first (Leverages Docker Cache?)
COPY requirements.txt .
# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cron \
    && rm -rf /var/lib/apt/lists/*

# Artifact to start configuring the venv
FROM base AS artifact
# Install Python dependencies globally (no venv)
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
# Copy the rest of the app
COPY . .
# Copy CRON job
COPY cron/cleanup_cron /etc/cron.d/cleanup_cron
# Give execution rights to the cron job file and Apply cron job
RUN chmod 0644 /etc/cron.d/cleanup_cron \
    && crontab /etc/cron.d/cleanup_cron
# Ensure cleanup script is executable
RUN chmod +x cron/cleanup_script.py

# Production image
FROM artifact AS prod
# Start Gunicorn and cron
CMD ["sh", "-c", "cron && gunicorn -w 4 -b 0.0.0.0:80 --reload 'app:create_app()'"]

# Dev image
FROM artifact AS dev
# Start Gunicorn and cron
CMD ["sh", "-c", "cron && gunicorn -w 4 -b 0.0.0.0:80 'app:create_app()'"]
