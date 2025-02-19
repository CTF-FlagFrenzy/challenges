# Behind the Pixels

Steganography challenge where you have to get the flag from a picture where the flag is in the metadata.
**Level**:Easy


## Challenge Overview:

In this challenge, you were tasked to find the flag within a picture. Good luck!

- Hint 1: Every file has a story to tell; some just need the right tool to read them.
- Hint 2: Information can be stored where you least expect it—try checking the metadata.
- Hint 3: Comments aren’t just for conversations; sometimes, they hide secrets.

---

### Docker Compose

Starting with the `docker-compose` file, this file starts the challenge container to set up the environment for the CTF.

```yml
services:
  exiftool-service:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: exiftool_container
    volumes:
      - .:/app
    restart: "no"

  file-server:
    build: .
    ports:
      - "8006:5000"
```

### Dockerfile

This Dockerfile sets up a Python environment with Flask and ExifTool installed, copies a Python script (`script.py`) and an image into the /app directory, and specifies that the container should run script.py when started.

```Dockerfile
FROM python:3.9-slim

RUN apt-get update && apt-get install -y exiftool && pip install flask

WORKDIR /app
RUN ls -l /app

COPY script.py .
COPY nice_holiday.JPG .

CMD ["python", "script.py"]
```

## Technical guideline

### Installation

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

Then you navigate to the folder `Behind_The_Pixels/challenge` and type the following command in the cli.

```
docker-compose up
```

Now you can see all running container with `docker ps`.  
The webserver should be accessable on the port specified in the docker-compose.yml.

**HAVE FUN**