# Shell Assembly

A challange where you have to upload a reverse shell script in assembly and use it to read some stuff
**Level**: Medium

### Docker Compose

- The `docker-compose.yml` file sets up the environment for the challenge by starting the docker container and running a few installation scripts

```yaml
services:
  alpine:
    network_mode: bridge
    build:
      context: ./Alpine
      dockerfile: Dockerfile
    environment:
      - KEY_FlagFrenzy=/uploads/assembly-script.asm
    container_name: alpine_server
    volumes:
      - ./dev/:/uploads/
    ports:
      - "3000:3000"
    command: /bin/sh /app/entrypoint.sh
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

### Dockerfile

- The Dockerfile gets an alpine container with an webserver that can upload stuff from https://github.com/TwoStoryRobot/docker-simple-file-upload


```yaml
FROM twostoryrobot/simple-file-upload

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install necessary packages and dependencies
RUN sh installation.sh

WORKDIR /code

```

### Entrypoint

- Due to the fact that starting the old container runs its own job, a script was used to start the upload and the file watcher service. The file watching works by starting a job that watches for filechanges, when it happens it runs a script to compile the assembly code and run it. After running it restarts the watching service.

```bash
#!/bin/sh

# Navigate to the code directory and start npm
cd /code
npm start &

# Run the inotifywait loop
while inotifywait -e close_write /uploads/; do
    sh /app/runAssembly.sh
done
```

### Run Assembly

- This script compiles, links and runs the uploaded assembly code. The elf64 syntax is used for the assembly file and the standard c libraries may be used for the code. 

```bash
#!/bin/sh
cd /uploads
# compile
nasm -f elf64 assembly-script.asm -o script.o
# link
ld script.o -o script -dynamic-linker /lib/ld-musl-x86_64.so.1 -lc
# run
./script
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

```
git pull https://github.com/CTF-FlagFrenzy/challenges.git
```

Then you navigate to the root of the `Shell_Assembly` challenge and type the following command in the cli.

```
docker-compose up
```

You can see all running container with `docker ps`.

**HAVE FUN**
