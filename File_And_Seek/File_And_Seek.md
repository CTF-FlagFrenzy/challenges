# File And Seek

Web challenge where you have to use tools to find a hidden file. 
**Level**: Medium

## Challenge Overview

In this challenge, participants need to find a hidden file within a web application. The hidden file contains information about various cryptocurrency products, and each product's ID section contains a part of the flag. The challenge involves using web enumeration tools to locate the hidden file and then extracting and assembling the flag from the product IDs.

## Implementation Details

### Docker Compose Configuration

The `docker-compose.yml` file sets up the environment for the challenge by building and running the Flask application:

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
      - TEAMKEY=XXXXXXX  # This value is replaced with a unique team key in the actual challenge
```

The TEAMKEY environment variable provides a unique value that is combined with the challenge key to generate a unique flag for each team.

### Dockerfile Implementation

The Dockerfile builds the Python environment for the Flask application:

```dockerfile
FROM python:3

# Copy and install requirements
COPY flask_app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and set working directory
COPY . code
WORKDIR /code

EXPOSE 80

# Run the Flask application
ENTRYPOINT ["python", "flask_app/app.py"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
```

The Dockerfile:
1. Uses a Python 3 base image
2. Installs the required dependencies (Flask and Werkzeug)
3. Copies the application code to the container
4. Exposes port 80 for web traffic
5. Sets up the entrypoint to run the Flask application

### Flask Application Architecture

The Flask application (`flask_app/app.py`) serves as the main entry point and has two primary routes:

```python
import subprocess
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route("/")
def index():
    # Generate the hidden file with the flag when the main page is accessed
    subprocess.run(["python", "flask_app/create_json.py"])
    return render_template("index.html")

@app.route("/security.txt")
def hidden_file():
    import os
    # Serve the hidden file containing the flag parts
    return send_from_directory(os.path.join(app.root_path, "hidden"), "security.txt")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
```

Key components:
1. `/` route - Serves the main index page and triggers flag generation
2. `/security.txt` route - Serves the hidden file containing the flag parts
3. The Flask application runs on port 80 inside the container

### Flag Generation Process

The heart of the challenge is the `create_json.py` script, which generates a unique flag and embeds it in product IDs:

```python
import hashlib
import json
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Load the product data from products.json
with open(os.path.join(os.path.dirname(__file__), "products.json"), "r") as json_file:
    data = json.load(json_file)
    products = data["products"]

# Generate a unique flag by combining challenge key and team key
challengeflag = "#74q$j&zcB"
teamflag = os.environ.get("TEAMKEY")
combined_flag = challengeflag + teamflag

if combined_flag:
    # Create a SHA-256 hash of the combined flag with the FF{...} format
    hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
    logger.info("Flag successfully created and hashed: %s", hashed_flag)
else:
    logger.error(
        "Failed to create flag. Ensure TEAMKEY and CHALLENGEKEY are set in environment variables."
    )
    hashed_flag = "FLAG_NOT_DEFINED"

# Split the flag into 9 parts to assign to each product
part_length = len(hashed_flag) // 9
hashed_flag_parts = [
    hashed_flag[i: i + part_length] for i in range(0, part_length * 8, part_length)
]
hashed_flag_parts.append(hashed_flag[part_length * 8:])

logger.info("Hashed flag parts created: %s", hashed_flag_parts)

# Assign each flag part as the ID of a product
for i, product in enumerate(products):
    try:
        product["id"] = hashed_flag_parts[i]
        logger.info(
            "Assigned ID %s to product %s", hashed_flag_parts[i], product["name"]
        )
    except IndexError:
        logger.error("Not enough hashed flag parts to assign to all products")
        break

# Save the updated product data to security.txt in the hidden directory
data = {"products": products}
output_path = os.path.join("flask_app/hidden", "security.txt")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as json_file:
    json.dump(data, json_file, indent=4)
logger.info("JSON file successfully created at %s", output_path)
```

Key flag generation steps:
1. Load product data from products.json
2. Combine the challenge key and team key to create a unique identifier
3. Generate a SHA-256 hash of the combined key, prefixed with "FF{"
4. Split the hash into 9 parts
5. Assign each part to a product as its ID
6. Save the modified product data to security.txt in the hidden directory

### Web Interface

The web interface is a simple cryptocurrency financial dashboard created with HTML, Tailwind CSS, and TradingView widgets:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Get Rich</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <script src="https://s3.tradingview.com/tv.js"></script>
    <!-- Additional styling -->
</head>
<body class="bg-solana-dark text-white">
    <!-- Header and main content -->
    <main class="container mx-auto p-4">
        <!-- Financial dashboard content -->
        <!-- Market overview section with TradingView charts -->
        <!-- Portfolio performance section -->
    </main>
    <footer class="bg-gray-800 p-4 text-center rounded-lg mt-4 w-full fixed bottom-0">
        <p class="text-gray-500">&copy; 2024 Financial Dashboard. All rights reserved.</p>
    </footer>
    <!-- TradingView widget initialization scripts -->
</body>
</html>
```

The web interface serves as a distraction, containing no direct hints to the existence of the hidden file.

## Challenge Solution

To solve this challenge, participants need to:

1. Use web enumeration tools like `ffuf`, `gobuster`, or `dirb` to discover the hidden `/security.txt` endpoint
2. Access the hidden file at `/security.txt`
3. Extract the product IDs from the JSON data
4. Concatenate the IDs in order to reconstruct the complete flag

### Data Files

The challenge uses a predefined `products.json` file containing information about 9 cryptocurrency products:

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
        // 8 more products...
    ]
}
```

When the challenge runs, these static product IDs are replaced with parts of the generated flag.

## Technical Implementation Guidelines

### Installation

> [!NOTE]
> Make sure to install docker and docker-compose first

**Linux**

- [Docker Linux installation](https://docs.docker.com/engine/install/ubuntu/)
- [Docker-compose Linux installation](https://docs.docker.com/compose/install/linux/)

**Windows**

- [Docker Windows installation](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Docker-compose Windows installation](https://docs.docker.com/compose/install/)

After installing Docker and Docker Compose, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/CTF-FlagFrenzy/challenges.git
   ```

2. Navigate to the File_And_Seek challenge directory:
   ```
   cd challenges/File_And_Seek
   ```

3. Start the challenge:
   ```
   docker-compose up
   ```

4. Verify the container is running:
   ```
   docker ps
   ```

The challenge will be accessible at http://localhost:80.

**HAVE FUN**

> [!NOTE]
> If you have any problems solving this challenge, you can find a full guide [here](https://github.com/CTF-FlagFrenzy/challenges/blob/main/File_And_Seek/writeup.md)