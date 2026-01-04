# Grab the Python3 Base
FROM python:3 AS base
# Switch to root user
USER root
# Install Apache2
RUN apt-get update \
    && apt-get install -y apache2 libapache2-mod-wsgi-py3 python3-venv
# Enable WSGI for Apache
RUN a2enmod wsgi \
    && a2enmod mpm_event
# Copy apache2 config
COPY ./apache2/apache2.conf /etc/apache2/apache2.conf 
COPY ./apache2/tunedgpt.conf /etc/apache2/sites-available/tunedgpt.conf
# Create the main apache2 config and delete the default
RUN rm -f /etc/apache2/sites-available/000-default.conf \
    && rm -f /etc/apache2/sites-available/000-ssl.conf \
    && a2ensite tunedgpt

# Artifact of our prod/dev environments    
FROM base AS artifact
# Set user to root
USER root
# Copy files to directory
COPY --chown=www-data:www-data ./ /var/www/TunedGPT
# Move into codebase
WORKDIR /var/www/TunedGPT
# Set up Python VENV
RUN python -m venv /var/www/TunedGPT/venv 
RUN /var/www/TunedGPT/venv/bin/pip install --upgrade pip \
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
# Switch to www-data
USER www-data

# prod environment
FROM artifact AS prod
# Set working dir to root of project
WORKDIR /var/www/TunedGPT
# Copy production .env 
COPY .env.prod .env
# Start the Server
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
# Switch to www-data
USER www-data