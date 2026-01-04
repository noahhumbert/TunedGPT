# Grab the Python3 Base
FROM python:3 AS BASE
# Switch to root user
USER root
# Install Apache2
RUN apt-get install -y apache2
# Enable WSGI for Apache
RUN a2enmod wsgi
# Copy apache2 config
COPY ./apache2/apache2.conf /etc/apache2/apache2.conf 
COPY ./apache2/tunedgpt.conf /etc/apache2/sites-available/tunedgpt.conf
# Create the main apache2 config and delete the default
RUN rm -f /etc/apache2/sites-available/000-default.conf \
    rm -f /etc/apache2/sites-available/000-ssl.conf \
    a2ensite tunedgpt
# Artifact of our prod/dev environments    
FROM BASE AS artifact
# Set user to root
USER root
# Copy files to directory
COPY --chown=www-data:www-data ./ /var/www/TunedGPT
# Move into codebase
WORKDIR /var/www/TunedGPT
# Set up Python VENV
RUN python -m venv /var/www/TunedGPT/venv \
    source .\venv\bin\activate \
    pip3 install -r requirements.txt
# Touch the .env file for future use
RUN touch .env \
    && chown www-data:www-data .env \
    && chmod ug+rw .env
# dev environment
FROM artifact as dev
# Run app.py
CMD [ "python", "./your-daemon-or-script.py" ]