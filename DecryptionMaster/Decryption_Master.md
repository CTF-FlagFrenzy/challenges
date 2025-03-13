# Decryption Master
Are you the Decryption Master that finds interesting information on the given system?
**Level**: Hard

## Challenge Overview
The Decryption Master challenge requires knowledge in various issues, such as Linux, Forensics as well as Cryptography. Only people with a clear mind are able to find the information hidden on the Linux system!

### Docker Compose
The given Docker Compose file provides a Ubuntu container that allows SSH access.
```yml
networks:
  encrpytion-forensics:

services:
  ubuntu-ssh:
    build:
      context: .
      dockerfile: Dockerfile
   
    ports:
      - "8080:22"

    networks:
      - encrpytion-forensics

    environment:
      - TEAMKEY=XXXXXXX
```

### Dockerfile
The Dockerfile sets up the Ubuntu system, e.g. OpenSSH is installed and configured.
```yml
FROM ubuntu:latest

COPY ./create_flags.py /root

RUN apt update && apt install -y openssh-server python3 python3-pip python3-venv
RUN useradd -m -s /bin/bash j007 && echo 'j007:Pa$$w0rd!' | chpasswd
RUN python3 -m venv /env && /env/bin/pip install pycryptodome

EXPOSE 22

ENTRYPOINT ["/bin/bash", "-c", "source /env/bin/activate && python3 /root/create_flags.py && rm /root/create_flags.py && service ssh start && sleep infinity"]
```

## Technical Guideline

### Installation

> [!NOTE]
> Make sure to install docker and docker-compose first

**Linux**

- [Docker Linux installation](https://docs.docker.com/engine/install/ubuntu/)

- [Docker-compose Linux installation](https://docs.docker.com/compose/install/linux/)

**Windows**

- [Docker Windows installation](https://docs.docker.com/desktop/setup/install/windows-install/)

- [Docker-compose Windows installation](https://docs.docker.com/compose/install/)

After you installed docker and docker-compose you need to pull the repository via cli using this command.

```
git pull https://github.com/CTF-FlagFrenzy/challenges.git
```

Then you navigate to the root of the `Decryption_Master` challenge and type the following command in the cli.

```
docker-compose up
```

You can see all running container with `docker ps`.

**HAVE FUN**

> [!NOTE]
> If you have any problems solving this challenge you can find a full guide here.