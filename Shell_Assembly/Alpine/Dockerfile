FROM twostoryrobot/simple-file-upload

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install necessary packages and dependencies
RUN sh installation.sh

WORKDIR /code
