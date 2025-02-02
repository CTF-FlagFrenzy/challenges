# Stealth Invoice
A forensics challenge that provides more than one flag!
**Level**: Medium

## Challenge Overview
In the "Stealth Invoice" challenge, participants must analyze a seemingly normal invoice PDF to uncover hidden information. The challenge involves finding and decoding secret messages embedded within the document.

### Docker Compose
Starting off with the `docker-compose` file, this file starts the challenge container needed for the CTF.

```yml
services:
  flask:
    build:
      context: .
      dockerfile: flask_app/Dockerfile

    ports:
      - '80:80'

    environment:
      - TEAMKEY=XXXXXXX
      - TEAM_ID=XXXXXXX
      - CHALLENGEKEY=#oLq3j&ZcF
      - CHALLENGEKEY2=M9LQXpX^Us
```

### Dockerfile
The Dockerfile sets up the Flask application environment.

```yml
FROM python:3

COPY . code
WORKDIR /code
RUN pip install --no-cache-dir -r flask_app/requirements.txt
EXPOSE 80

ENTRYPOINT ["python", "flask_app/app.py"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
```

### Flask Application
The Flask application is defined in `flask_app/app.py`. It serves the download for the PDF file.

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

Then you navigate to the root of the `Stealth_Invoice` challenge and type the following command in the cli.

```
docker-compose up
```

You can see all running container with `docker ps`.

**HAVE FUN**

> [!NOTE]
> If you have any problems solving this challenge you can find a full guide [here](https://github.com/CTF-FlagFrenzy/challenges/blob/main/Stealth_Invoice/writeup.md)