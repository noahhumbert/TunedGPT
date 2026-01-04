# Ubuntu Base
FROM ubuntu:22.04 AS base
# Switch to root user
USER root
# Install apache2
RUN apt-get update \
    && apt-get install -y apache2 apache2-bin apache2-utils  python3-venv
# Copy apache2 configs
COPY ./apache2/apache2.conf /etc/apache2/apache2.conf 
COPY ./apache2/tunedgpt.conf /etc/apache2/sites-available/tunedgpt.conf
# Delete the old apache2 configs. Enable the new ones and enable sites and mods
RUN rm -f /etc/apache2/sites-available/000-default.conf \
    && rm -f /etc/apache2/sites-available/000-ssl.conf \
    && a2dismod mpm_prefork mpm_worker || true \
    && a2enmod mpm_event \
    && a2ensite tunedgpt 
# Artifact
FROM base AS artifact
# Root user
USER root
# Copy files to directory
COPY --chown=www-data:www-data ./ ./var/www/TunedGPT
# Move to the new codebase
WORKDIR /var/www/TunedGPT
# Force noninteractive APT and set timezone
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC
# Set up Python VENV
RUN python3 -m venv /var/www/TunedGPT/venv \
    && /var/www/TunedGPT/venv/bin/pip install --upgrade pip \
    && /var/www/TunedGPT/venv/bin/pip install -r /var/www/TunedGPT/requirements.txt
# Touch the .env file for future use
RUN touch .env \
    && chown www-data:www-data .env \
    && chmod ug+rw .env

# dev environment
FROM artifact AS dev
# Set working dir to root of project
WORKDIR /var/www/TunedGPT
# Copy dev env over env
COPY .env.dev .env
# Start the Server
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]

# prod environment
FROM artifact AS prod
# Set working dir to root of project
WORKDIR /var/www/TunedGPT
# Copy production .env 
COPY .env.prod .env
# Start the Server
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
