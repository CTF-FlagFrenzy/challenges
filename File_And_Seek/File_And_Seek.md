# File And Seek

Web challenge where you have to use tools to find a hidden file. 
**Level**: Medium

## Challenge Overview

In this challenge, participants need to find a hidden file within a web application. The hidden file contains information about various products, and each product's ID section contains a part of the flag. The challenge involves using web tools and techniques to locate and assemble the flag.

### Docker Compose

- The `docker-compose.yml` file sets up the environment for the challenge by starting the Flask service.

```yaml
version: '3'

volumes:
  my-django-data:

services:
  flask:
    build:
      context: .
      dockerfile: flask_app/Dockerfile

    ports:
      - '8003:5000'

    environment:
      - TEAMKEY=XXXXXXX
      - CHALLENGEKEY=#74q$j&zcB
```

### Dockerfile

- The Dockerfile sets up the Flask application environment.

```yaml
FROM python:3

COPY [requirements.txt](http://_vscodecontentref_/0) ./
RUN pip install --no-cache-dir -r [requirements.txt](http://_vscodecontentref_/1)

COPY . /code
WORKDIR /code

ENTRYPOINT ["python", "flask_app/app.py"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
```

### Flask Application

- The Flask application is defined in `flask_app/app.py`. It serves the main page and the hidden file.

```py
import subprocess

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route("/")
def index():
    subprocess.run(["python", "flask_app/create_json.py"])
    return render_template("index.html")

@app.route("/security.txt")
def hidden_file():
    import os
    return send_from_directory(os.path.join(app.root_path, "hidden"), "security.txt")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

### JSON File Creation

- The `create_json.py` script generates a JSON file with product information and saves it to a hidden directory.

```py
import os
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

products = [
    {"name": "Product 1", "description": "Description 1"},
    {"name": "Product 2", "description": "Description 2"},
    # Add more products as needed
]

hashed_flag = "hashed_flag_value"
part_length = len(hashed_flag) // 8
hashed_flag_parts = [
    hashed_flag[i: i + part_length] for i in range(0, part_length * 8, part_length)
]
hashed_flag_parts.append(hashed_flag[part_length * 8:])

logger.info("Hashed flag parts created: %s", hashed_flag_parts)

for i, product in enumerate(products):
    try:
        product["id"] = hashed_flag_parts[i]
        logger.info(
            "Assigned ID %s to product %s", hashed_flag_parts[i], product["name"]
        )
    except IndexError:
        logger.error("Not enough hashed flag parts to assign to all products")
        break

data = {"products": products}

output_path = os.path.join("flask_app/hidden", "security.txt")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as json_file:
    json.dump(data, json_file, indent=4)
logger.info("JSON file successfully created at %s", output_path)
```

### HTML Template

- The HTML template for the main page is located in `flask_app/templates/index.html`.

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

After you installed docker and docker-compose you need to pull the repository via cli using this command.

```
git pull https://github.com/CTF-FlagFrenzy/challenges.git
```

Then you navigate to the root of the `Solana Assests` challenge and type the following command in the cli.

```
docker-compose up
```

You can see all running container with `docker ps`.

**HAVE FUN**

> [!NOTE]
> If you have any problems solving this challenge you can find a full guide [here](https://github.com/CTF-FlagFrenzy/challenges/blob/main/File_And_Seek/writeup.md)