# PYCked Apart
> _This challenge is called `PYCked Apart`, but you may also see it referred to as it's working name `Pydetect` in some places._

Reversing challenge where you have to decompile a python script, to find out how the flag is stored in a file.
**Level**: Easy

## Challange Overview

### Docker Compose
 - The `compose.yml` starts the challange container, setting up the required files and providing them via a download.

```yaml
version: '3'
services:
  python:
    build: .
    ports:
      - '80:80'
    environment:
      - TEAMKEY=TeamKey
      - CHALLENGEKEY=01JEB55RPNPJW08X1GB5SR03DF
```

### Dockerfile 

- The Dockerfile defines how to build the container required to play this challange.

```Dockerfile
FROM python:3.12

COPY . c
WORKDIR /c

RUN bash build.sh

EXPOSE 80

ENTRYPOINT [ "bash", "entry.sh" ]
```

The Dockerfile uses the `build.sh` script to run all the build instructions

```bash
#!/usr/bin/env bash

apt update
apt install zip -y
```

### Challange Scripts

- The file `entry.sh` runs the `main.py` python script and starts the http server to serve the required files.

`entry.sh`
```bash
#!/usr/bin/env bash

python3 main.py

zip solveme.zip encoder.pyc flag
mv solveme.zip ./webroot/solveme.zip

cd webroot
python3 -m http.server 80
```

`main.py`
```py
import hashlib, os, zlib, base64, pickle

teamkey = os.getenv("TEAMKEY")
challenge = os.getenv("CHALLENGEKEY")

flag = "%s%s" % (teamkey, challenge)
flaghash = (hashlib.sha256(flag.encode()).hexdigest())
hashed_flag = "FF{%s}" % flaghash

enc = base64.urlsafe_b64encode(zlib.compress(bytes(hashed_flag, 'utf-8')))
with open('flag', 'wb') as f:
    pickle.dump(enc, f)
```


### Installation

> [!NOTE]
> Make sure to install docker and docker-compose first

**Linux**

- [Docker Linux installation](https://docs.docker.com/engine/install/ubuntu/)

- [Docker-compose Linux installation](https://docs.docker.com/compose/install/linux/)

**Windwos**

- [Docker Windows installation](https://docs.docker.com/desktop/setup/install/windows-install/)

- [Docker-compose Windows installation](https://docs.docker.com/compose/install/)

After you installed docker and docker-compose you need to pull the repository via cli using this command.

```sh
git pull https://github.com/CTF-FlagFrenzy/challenges.git
```

Then you navigate to the root of the `PYCked Apart` challenge, located at the `Pydetect/` directory and type the following command in the cli.

```sh
docker-compose up
```

You can see all running container with `docker ps`.

**HAVE FUN**