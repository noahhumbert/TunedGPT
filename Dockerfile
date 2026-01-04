# Base image
FROM ubuntu:22.04 AS base
# Switch to root
USER root
# Install Apache, mod_wsgi, Python, pip, and required tools
RUN apt-get update && apt-get install -y \
    apache2 \
    libapache2-mod-wsgi-py3 \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# Set working directory for Flask app
WORKDIR /var/www/tunedgpt
# Copy app
COPY . .

FROM base AS artifact
# Copy requirements and install
RUN python3 -m venv venv \
    && ./venv/bin/pip install --upgrade pip \
    && ./venv/bin/pip install -r requirements.txt
# Set up Apache config
COPY apache2/tunedgpt.conf /etc/apache2/sites-available/000-default.conf
# Enable mod_wsgi (should already be enabled with libapache2-mod-wsgi-py3)
RUN a2enmod wsgi

# Dev Environment
FROM artifact AS dev
# Copy env file
COPY .env.dev .env
# Start Apache in the foreground
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
# Prod Environment

FROM artifact AS prod
# Copy env file
COPY .env.prod .env
# Start Apache in the foreground
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
