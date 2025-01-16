# Use the official Alpine image as the base image
FROM twostoryrobot/simple-file-upload

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install necessary packages and dependencies
RUN sh installation.sh

EXPOSE 80

WORKDIR /code

# Run a simple command to keep the container running
# CMD ["sh", "-c", "while true; do sleep 3600; done"]