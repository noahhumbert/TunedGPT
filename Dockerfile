# Base image: official Apache HTTPD
FROM httpd:2.4 AS base

# Switch to root
USER root

# Install Python 3 and venv
RUN apt-get update \
    && apt-get install -y python3 python3-venv python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy Apache configs
COPY ./apache2/apache2.conf /usr/local/apache2/conf/httpd.conf
COPY ./apache2/tunedgpt.conf /usr/local/apache2/conf/extra/tunedgpt.conf

# Include the tunedgpt site in main Apache config
RUN echo 'Include conf/extra/tunedgpt.conf' >> /usr/local/apache2/conf/httpd.conf

# Artifact stage: copy application
FROM base AS artifact

# Create app directory
WORKDIR /usr/local/apache2/htdocs/TunedGPT
COPY --chown=www-data:www-data ./ ./ 

# Set up Python virtual environment
RUN python3 -m venv /usr/local/apache2/htdocs/TunedGPT/venv \
    && /usr/local/apache2/htdocs/TunedGPT/venv/bin/pip install --upgrade pip \
    && /usr/local/apache2/htdocs/TunedGPT/venv/bin/pip install -r /usr/local/apache2/htdocs/TunedGPT/requirements.txt

# Touch .env for future use
RUN touch .env \
    && chown www-data:www-data .env \
    && chmod ug+rw .env

# Dev environment
FROM artifact AS dev
WORKDIR /usr/local/apache2/htdocs/TunedGPT
COPY .env.dev .env
# Run Apache in foreground
CMD ["httpd-foreground"]

# Prod environment
FROM artifact AS prod
WORKDIR /usr/local/apache2/htdocs/TunedGPT
COPY .env.prod .env
CMD ["httpd-foreground"]
