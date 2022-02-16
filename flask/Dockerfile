# Use the Python3.x image
ARG PYTHON_VER=3.9
FROM python:${PYTHON_VER}

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app 
ADD . /app

ENV HTTP_PROXY http://fdcproxy.1dc.com:8080
ENV HTTPS_PROXY http://fdcproxy.1dc.com:8080

# Install the dependencies
RUN pip install -r requirements.txt

# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]