# Shadow File

## Challenge Overview

In this challenge, participants must find a hidden file within a web application. The hidden file contains information about various cryptocurrency products, and each product's ID section holds a part of the flag. These flag parts are hex-encoded and shuffled, and the "units" field in each product contains the information needed to arrange the parts in the correct order. The challenge involves web reconnaissance techniques to locate the hidden file and cryptographic knowledge to decode and reassemble the flag.

### Challenge Mechanics

1. Participants must discover the hidden endpoint `/security.txt`
2. The endpoint serves a JSON file with product information
3. Each product has an ID (hex-encoded part of the flag) and a units value (position indicator)
4. Participants need to decode each ID and arrange them according to the units values
5. The assembled text forms the flag in the format `FF{hash}`

## Technical Implementation

### Docker Compose

The `docker-compose.yml` file sets up the environment for the challenge by starting the Flask service on port 80:

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
      - '80:80'

    environment:
      - TEAMKEY=XXXXXXX
```

### Dockerfile

The Dockerfile sets up the Flask application environment:

```dockerfile
FROM python:3

COPY flask_app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . code
WORKDIR /code
EXPOSE 80

ENTRYPOINT ["python", "flask_app/app.py"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
```

### Requirements

The application depends on Flask and Werkzeug:

```
Flask==2.0.2
Werkzeug==2.0.3
```

### Flask Application

The Flask application is defined in `flask_app/app.py`. It serves the main page and the hidden file:

```python
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
    app.run(host="0.0.0.0", port=80)
```

### Product Data

The application uses a JSON file with product information as a base:

```json
{
    "products": [
        {
            "id": "535551674e444935",
            "name": "Bitcoin Paper Wallet (pack of 20)",
            "description": "Securely store your Bitcoin with these paper wallets.",
            "picture": "/static/img/products/bitcoin_paper_wallet.png",
            "priceUsd": {
                "currencyCode": "USD",
                "units": 50
            },
            "categories": ["crypto", "security"]
        },
        // ...more products...
    ]
}
```

### Flag Generation Script

The `create_json.py` script is responsible for generating the challenge flag and hiding it within the product data:

```python
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

challengeflag = "t9gE6@W!Nz"
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
    hashed_flag[i: i + part_length] for i in range(0, part_length * 8, part_length)
]
hashed_flag_parts.append(hashed_flag[part_length * 8:])

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

The script performs the following key operations:

1. **Reads the product data**: Loads the base product information from products.json
2. **Creates the flag**: Combines the challenge key with the team key and creates a SHA-256 hash
3. **Splits the flag**: Divides the flag into 9 parts of equal length
4. **Encodes and shuffles**: Converts each part to hexadecimal and randomly shuffles them
5. **Embeds the flag parts**: Assigns each encoded part to a product's ID and stores its original position in the units field
6. **Saves the modified data**: Writes the JSON data to the hidden file location

### Frontend Implementation

The HTML template (`index.html`) creates a financial dashboard as a decoy, showing cryptocurrency charts to maintain the theme while hiding the actual challenge:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Get Rich</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <script src="https://s3.tradingview.com/tv.js"></script>
    <style>
        .bg-solana-dark { background-color: #131722; }
        .text-solana { color: #00FFA3; }
        .hover\:text-solana:hover { color: #00FFA3; }
    </style>
</head>
<body class="bg-solana-dark text-white">
    <!-- Frontend for financial dashboard -->
    <!-- Contains charts from TradingView -->
</body>
</html>
```

## Solving the Challenge

To solve this challenge, participants need to:

1. **Discover the hidden endpoint**: Use tools like `ffuf` or directory brute-forcing to find `/security.txt`
2. **Extract the encoded flag parts**: Retrieve each product's ID from the JSON data
3. **Decode the hex values**: Convert the hex-encoded IDs back to text
4. **Determine the correct order**: Use the "units" value in each product to determine the position of each part
5. **Assemble the flag**: Combine all parts in the correct order to form the flag

The final flag will be in the format: `FF{<sha256_hash>}`

## Technical Requirements

### Installation

> [!NOTE]
> Make sure to install docker and docker-compose first

**Linux**

- [Docker Linux installation](https://docs.docker.com/engine/install/ubuntu/)
- [Docker-compose Linux installation](https://docs.docker.com/compose/install/linux/)

**Windows**

- [Docker Windows installation](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Docker-compose Windows installation](https://docs.docker.com/compose/install/)

After installing Docker and Docker Compose, you need to clone the repository:

```
git clone https://github.com/CTF-FlagFrenzy/challenges.git
```

Then navigate to the root of the `Shadow_File` challenge and run:

```
docker-compose up
```

You can view running containers with `docker ps`.

**HAVE FUN**

> [!NOTE]
> If you have any problems solving this challenge, you can find a detailed writeup [here](https://github.com/CTF-FlagFrenzy/challenges/blob/main/Shadow_File/writeup.md)