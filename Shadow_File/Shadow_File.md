# Shadow File

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
      - '8007:5000'

    environment:
      - TEAMKEY=XXXXXXX
      - CHALLENGEKEY=t9gE6@W!Nz
```

### Dockerfile

- The Dockerfile sets up the Flask application environment.

```yml
FROM python:3

COPY  ./
RUN pip install --no-cache-dir -r 

COPY . code
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

- The `create_json.py` script is responsible for generating a JSON file with product information and saving it to a hidden directory. This script performs several key tasks:

- Logging Configuration: Sets up logging to capture and display information about the script's execution.

- Loading Product Data: Reads product data from a JSON file.

- Flag Generation: Combines environment variables to create a flag, hashes it, and splits it into parts.

- Encoding and Shuffling: Encodes the flag parts to hexadecimal, shuffles them, and assigns them to products.

- Saving the JSON File: Writes the modified product data to a hidden file.
Here is the detailed code:

```py
import hashlib
import json
import logging
import os
import random

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

with open(os.path.join(os.path.dirname(__file__), "products.json"), "r") as json_file:
    data = json.load(json_file)
    products = data["products"]

challengeflag = os.environ.get("CHALLENGEKEY")
teamflag = os.environ.get("TEAMKEY")
combined_flag = challengeflag + teamflag

if combined_flag:
    hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
    logger.info("Flag successfully created and hashed: %s", hashed_flag)
else:
    logger.error(
        "Failed to create flag. Ensure TEAMKEY and CHALLENGEKEY are set in environment variables."
    )

part_length = len(hashed_flag) // 9
hashed_flag_parts = [
    hashed_flag[i: i + part_length] for i in range(0, part_length * 9, part_length)
]
hashed_flag_parts.append(hashed_flag[part_length * 9:])

logger.info("Hashed flag parts created: %s", hashed_flag_parts)

# Encode each part to hex using NONE as the delimiter
hashed_flag_parts_hex = [part.encode("utf-8").hex() for part in hashed_flag_parts]

# Shuffle the encoded parts and keep track of the original positions
original_positions = list(range(len(hashed_flag_parts_hex)))
shuffled_positions = original_positions[:]
random.shuffle(shuffled_positions)

shuffled_flag_parts_hex = [hashed_flag_parts_hex[i] for i in shuffled_positions]

logger.info("Shuffled hashed flag parts: %s", shuffled_flag_parts_hex)
logger.info("Shuffled positions: %s", shuffled_positions)

for i, product in enumerate(products):
    try:
        product["id"] = shuffled_flag_parts_hex[i]
        product["priceUsd"]["units"] = shuffled_positions[i]  # Store the original position in the existing units field
        logger.info(
            "Assigned ID %s to product %s with units %d",
            shuffled_flag_parts_hex[i],
            product["name"],
            shuffled_positions[i],
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
> If you have any problems solving this challenge you can find a full guide [here](https://github.com/CTF-FlagFrenzy/challenges/blob/main/Shadow_File/writeup.md)