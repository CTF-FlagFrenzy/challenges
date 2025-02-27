# Phantom Frequency
> _This challenge is called `Phantom Frequency`, but you may also see it referred to as it's working name `morse` in some places._

Forensics challenge, where you have to find a not audible morse code flag.

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
      - CHALLENGEKEY=01JHQ6WHZMBCSEGDTF9Y8YFC99
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

- The file `entry.sh` runs the `main.py` python script, to generate the flag, the `padder.py` script to pad the audio files to be the same length, merges both with `ffmpeg`, this also decreases the volume of the flag file to achieve this challenge, and finally starts the http server to serve the combined audio file `intercepted.wav`.

- The two audio files in question contain a normal, audible decoy message, hinting at the inclusion of a second message, that is normally not audible. _Some truths whisper, barely a breath above silence. Only those who listen beyond the range of hearing will find the key._, the other message is at 20kHz, has decreased Volume and just encodes the hash of the flag.

`entry.sh`
```sh
#!/usr/bin/sh

python3 main.py
python3 padder.py

ffmpeg -i base_pad.wav -i tones_pad.wav -filter_complex "[0:a]volume=1.0[a0];[1:a]volume=0.1[a1];[a0][a1]amix=inputs=2" -ac 1 ./webroot/intercepted.wav

cd webroot/
python3 -m http.server 80
```

`main.py`
```py
import pycw
import os
import hashlib

challengekey = os.getenv('CHALLANGEKEY')
teamkey = os.getenv('TEAMKEY')

flaghash = hashlib.sha256(('%s%s' % (teamkey, challengekey)).encode()).hexdigest()
flag = 'FF{%s}' % flaghash

pycw.output_wave('tones.wav', flaghash, 24, 20000)
#pycw.output_wave('base.wav', 'Some truths whisper, barely a breath above silence. Only those who listen beyond the range of hearing will find the key.', 24, 500)
```

`padder.py`
```py
from pydub import AudioSegment

# Load the audio files
tones = AudioSegment.from_wav("tones.wav")
base = AudioSegment.from_wav("base.wav")

# Get the duration of each audio file in milliseconds
tones_duration = len(tones)
base_duration = len(base)

# Find the longer duration
duration = max(tones_duration, base_duration)

# Pad the shorter audio file with silence
tones = tones + AudioSegment.silent(duration=duration - tones_duration)
base = base + AudioSegment.silent(duration=duration - base_duration)

# Export padded Soundfiles
tones.export("tones_pad.wav", format="wav")
base.export("base_pad.wav", format="wav")
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

Then you navigate to the root of the `Phantom Frequency` challenge, located at the `morse/` directory and type the following command in the cli.

```sh
docker-compose up
```

You can see all running container with `docker ps`.

**HAVE FUN**