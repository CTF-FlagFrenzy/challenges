# Transmission Received

Forensics challenge, where you have to identify and decode a SSTV signal

## Challenge Overview

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
      - CHALLENGEKEY=01JN3EADQF59H8SQ2KDC51V5HW
```

### Dockerfile 

- The Dockerfile defines how to build the container required to play this challange.

```Dockerfile
FROM python:3.12

COPY . c
WORKDIR /c

RUN sh ./build.sh

EXPOSE 80

ENTRYPOINT [ "sh", "entry.sh" ]
```

The Dockerfile uses the `build.sh` script to run all the build instructions.

```sh
#!/usr/bin/sh

apt update
apt install ffmpeg -y

python3 -m pip install -r requirements.txt
```

### Challange Scripts

- The file `entry.sh` runs the `main.py` python script, to generate the flag and the QR-Code containing it, and superimposes the QR-Code onto a background image.
- Next it runs `pysstv` to convert the image into an SSTV transmission.
- Before the file can be served; `ffmpeg` is used to decrase the Volume. This is done, as otherwise the audio may clip and distort. Distortions may impact the abillity to correctly decode the Signal. 
- The final file is served as `transmission.wav`. 

`entry.sh`
```sh
#!/usr/bin/sh

python3 main.py
python3 -m pysstv --mode Robot36 placed.png ./transmission.wav
ffmpeg -i transmission.wav -filter:a "volume=0.1" ./webroot/transmission.wav

cd webroot/
python3 -m http.server 80
```

`main.py`
```py
import PIL.Image
import qrcode
import os
import hashlib

challengekey = '01JN3EADQF59H8SQ2KDC51V5HW'
teamkey = os.getenv('TEAMKEY')

flaghash = hashlib.sha256(('%s%s' % (challengekey, teamkey)).encode()).hexdigest()
print (flaghash)
flag = 'FF{%s}' % flaghash

code = qrcode.QRCode(box_size=4, border=1)
code.add_data(flag)
code.make(fit=False)
im = code.make_image()
#im.show()

fgimage = im.get_image()
bgimage = PIL.Image.open('bg.png')

bgimage.paste(fgimage, (82, 67))
bgimage.save('placed.png')
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

Then you navigate to the root of the `Transmission Received` challenge directory and type the following command in the cli.

```sh
docker-compose up
```

You can see all running container with `docker ps`.

**HAVE FUN**