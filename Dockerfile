# Use base image with Python 3.9 (note: the tag mentions 3.9 instead of 3.12)
FROM python:3.9-slim

# Install necessary packages for compiling C dependencies and OpenCV
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk2.0-dev \
    libboost-python-dev \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean

# Set the working directory
WORKDIR /app/src

# Copy only requirements.txt to cache dependency installation layers
COPY requirements.txt ..

# Install dependencies before copying project code
RUN pip install --upgrade pip && pip install -r ../requirements.txt

# Copy project files from the current directory to the image's current directory
COPY models ../models
COPY resources ../resources
ENV PYTHONPATH=/app:/app/src

COPY src .
COPY config.py ..
COPY token.txt ..

# Specify the command to run the application
CMD ["sh", "-c", "python main.py || sleep infinity"]
