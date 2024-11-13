# Solana Assest

Introductory challaenge into cryptography  
**Level**: Easy

## Challenge Overview:

  - The attacker needs to open a webpage and decode the shown string


---

### Docker Compose

Starting with the `docker-compose` file, this file starts the challenge container to set up the environment for the CTF.


```yml
version: '3'

services:
  web:
    build: .
    ports:
      - '7070:80'
    environment:
      - TEAMKEY=team1
      - CHALLENGE=heheheha
```


### Dockerfile

This file sets up the container

```Dockerfile
FROM httpd:latest

# Install Python
RUN apt-get update && apt-get install -y python3

# Copy the startup script and Python script
COPY ./start.sh /usr/local/bin/start.sh
COPY ./script.py /usr/local/bin/script.py
COPY ./requirements.txt /usr/local/bin/requirements.txt
# Make the startup script executable
RUN chmod +x /usr/local/bin/start.sh

# Set the entrypoint to the startup script
ENTRYPOINT ["/usr/local/bin/start.sh"]

EXPOSE 80
```

### script.sh

This creates a python environment, runs the dynamic flag script and starts the webserver

```sh
#!/bin/bash

# Update package list and install python3-venv if not already installed
apt-get update && apt-get install -y python3-venv

# Create a virtual environment
python3 -m venv /usr/local/bin/venv

# Activate the virtual environment
source /usr/local/bin/venv/bin/activate

# Install required packages
pip install -r /usr/local/bin/requirements.txt

# Run the Python script
python /usr/local/bin/script.py

# Start Apache server
httpd-foreground
```


## Technical guideline

### Installation

> [!NOTE]
> Make sure to install docker and docker-compose first

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

Then you navigate to the root of the `Ceasar_Cypher` challenge and type the following command in the cli.

```
docker-compose up
```

Now you can see all running container with `docker ps`.  
The webserver should be accessable on the port specified in the docker-compose

**HAVE FUN**



