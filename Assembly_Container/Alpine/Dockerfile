# Use the official Alpine image as the base image
FROM alpine:latest

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN sh installation.sh

# Run a simple command to keep the container running
CMD ["sh", "-c", "while true; do sleep 3600; done"]