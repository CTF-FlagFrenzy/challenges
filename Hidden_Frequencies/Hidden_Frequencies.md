# Hidden_Frequencies

Steganography-Challenge where 1 flag is hidden in a audio file. To get it one has to make several steps.

**Level**: Medium

## Challenge Overview:

A simple image can hide more than just colors and pixels. Your task is to uncover the secrets buried within. Dig deep, extract what’s hidden, and listen carefully—you might see the answer.

- Hint 1: Not everything in a file is visible at first glance. Sometimes, reading between the lines helps.
- Hint 2: The key is already there, just waiting to be read. The last few words might be your way in.
- Hint 3: Sounds can reveal secrets in unexpected ways—try looking at them instead of just listening.

### Docker Compose

Starting with the `docker-compose` file, this file starts the challenge container to set up the environment for the CTF.

```yml
version: '3'
services:
  challenge:
    build: challenge/
    ports:
      - "80:80"
    restart: unless-stopped
```

### Dockerfile

This Dockerfile sets up a lightweight Python environment with Flask, copies a Python script (script.py) and an image (hidden_frequencies.bmp) into the /app directory, and ensures that the container runs script.py when started. Additionally, it exposes port 80 for web access.

```Dockerfile
# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy necessary files
COPY script.py .
COPY hidden_frequencies.bmp .

# Install dependencies
RUN pip install flask

# Expose port 5000
EXPOSE 80

# Run the server
CMD ["python", "script.py"]
```

## Technical guideline

> [!NOTE]
> Make sure to install docker and docker-compose first.

**Linux**

- [Docker Linux installation](https://docs.docker.com/engine/install/ubuntu/)

- [Docker-compose Linux installation](https://docs.docker.com/compose/install/linux/)

**Windwos**

- [Docker Windows installation](https://docs.docker.com/desktop/setup/install/windows-install/)

- [Docker-compose Windows installation](https://docs.docker.com/compose/install/)

After installing Docker and Docker Compose, pull the repository via the CLI using the following command:
```
git pull https://github.com/CTF-FlagFrenzy/challenges.git
```

Then you navigate to the folder `Hidden_Frequencies/` and type the following command in the cli.

```
docker-compose up
```

Now you can see all running container with `docker ps`.  
The webserver should be accessable on the port specified in the docker-compose.yml and will download the file as soon as accessed.

**HAVE FUN**