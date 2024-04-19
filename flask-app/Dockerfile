# Use the official Python image with Ubuntu 22.04 support
FROM python:3.9

# Set environment variable to avoid buffering issues
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt requirements.txt
RUN apt-get update
RUN pip install --no-cache-dir -r requirements.txt

# Copy all other files into the container
COPY . .

# Add necessary metadata
LABEL maintainer="Daniil Bulgakov <d.bulgakov@gmail.com>"
LABEL description="Basic flask back-end app for ECG ESP32"

# Run the Flask application using the built-in development server
CMD ["flask", "run", "--host=0.0.0.0"]

