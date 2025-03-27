# Pixel Spy

Web challenge where you have to use tools to find a message in the image.
**Level**: Easy

## Challenge Overview

In this challenge, participants need to find a hidden message within an image. The hidden message contains the flag, and participants must use image analysis tools to extract it. The flag is hidden within the EXIF metadata of the image, specifically in the ImageDescription field.

## Technical Details

### Docker Compose

- The `docker-compose.yml` file sets up the environment for the challenge by starting the Flask service.

```yml
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

- The Dockerfile sets up the Flask application environment.

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

### Dependencies

The application requires the following Python packages:

```txt
Flask==2.0.2
Werkzeug==2.0.3
piexif==1.1.3
```

### Flask Application

- The Flask application is defined in `app.py`. It serves the main page and processes the image.

```python
import logging
import os
import subprocess

from flask import Flask, render_template

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/")
def home():
    # Path to the existing image
    os.path.join(os.path.dirname(__file__), "hacker.jpg")

    # Modify the image
    try:
        subprocess.run(
            ["python", os.path.join(os.path.dirname(__file__), "modify_image.py")],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Error modifying image: {e}")
        return "Error modifying image", 500

    # Path to the modified image
    os.path.join("static", "image_with_flag.jpg")

    # Use a relative URL for the image
    image_url = "/static/image_with_flag.jpg"

    return render_template("index.html", image_url=image_url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
```

### Image Modification Script

- The `modify_image.py` script modifies the image to include the hidden message. It embeds the flag into the EXIF metadata of the image.

```python
import hashlib
import logging
import os

import piexif

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

challengeflag = "T1#mXeG24B"
teamflag = os.environ.get("TEAMKEY")
combined_flag = challengeflag + teamflag if challengeflag and teamflag else None

if combined_flag:
    hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
    logger.info("Flag successfully created and hashed: %s", hashed_flag)
else:
    logger.error(
        "Failed to create flag. Ensure TEAMKEY and CHALLENGEKEY are set in environment variables."
    )
    hashed_flag = "FLAG_NOT_DEFINED"

# Define the paths
base_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_dir, "hacker.jpg")
static_dir = os.path.join(base_dir, "static")
modified_image_path = os.path.join(static_dir, "image_with_flag.jpg")

# Load the existing image
if not os.path.exists(image_path):
    logger.error(f"Image not found at path: {image_path}")
    raise FileNotFoundError(f"Image not found at path: {image_path}")

# Load the image and its EXIF data
try:
    exif_dict = piexif.load(image_path)
except ValueError as e:
    if str(e) == "doesnot have exif":
        logger.info("Image does not have EXIF data, creating new EXIF data.")
        exif_dict = {
            "0th": {},
            "Exif": {},
            "GPS": {},
            "Interop": {},
            "1st": {},
            "thumbnail": None,
        }
    else:
        raise

# Add the flag to the image metadata
exif_dict["0th"][piexif.ImageIFD.ImageDescription] = hashed_flag
exif_bytes = piexif.dump(exif_dict)

# Ensure the static directory exists
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# Save the modified image with metadata
piexif.insert(exif_bytes, image_path, modified_image_path)

logger.info(
    "Flag successfully added to the image metadata and saved as: %s",
    modified_image_path,
)
```

### HTML Template

- The HTML template for the main page is located in `index.html`. It creates a dramatic "hacker" aesthetic and displays the image that contains the hidden flag.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WELCOME</title>
    <style>
        body {
            background-color: #0d0d0d;
            color: #00ff00;
            font-family: 'Courier New', Courier, monospace;
            text-align: center;
        }
        h1 {
            margin-top: 50px;
            font-size: 3em;
        }
        img {
            margin-top: 20px;
            border: 5px solid #00ff00;
        }
        .skull {
            width: 100px;
            height: 100px;
            margin: 10px;
        }
        .skulls {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
        }
    </style>
</head>
<body>
    <h1>Welcome to the Dark Web</h1>
    <div class="skulls">
        <img src="https://img.icons8.com/ios-filled/100/00ff00/skull.png" alt="Hacker Skull" class="skull">
        <img src="https://img.icons8.com/ios-filled/100/00ff00/skull.png" alt="Hacker Skull" class="skull">
        <img src="https://img.icons8.com/ios-filled/100/00ff00/skull.png" alt="Hacker Skull" class="skull">
        <img src="https://img.icons8.com/ios-filled/100/00ff00/skull.png" alt="Hacker Skull" class="skull">
        <img src="https://img.icons8.com/ios-filled/100/00ff00/skull.png" alt="Hacker Skull" class="skull">
    </div>
    <img src="{{ image_url }}" alt="AI Generated Image">
</body>
</html>
```

## Challenge Solution

When a user visits the web page, they will see an image displayed. The goal is to download this image and analyze its metadata to find the hidden flag.

### Solution Steps:

1. **Access the webpage**: Navigate to the provided URL (localhost:80 when running locally)
2. **Download the image**: Right-click on the image and save it to your computer
3. **Examine the metadata**: There are several ways to view EXIF metadata:
   - Use a text editor like Notepad to open the file and search for "FF{"
   - Use online EXIF viewers (like exif.regex.info or exifdata.com)
   - Use command-line tools like `exiftool` with the command: `exiftool -ImageDescription image_with_flag.jpg`

The flag will be found in the ImageDescription field in the format `FF{hash}`, where the hash is a SHA-256 hash of the combined challenge flag and team key.

## Setting Up the Challenge

### Installation Requirements

> [!NOTE]
> Make sure to install docker and docker-compose first

**Linux**

- [Docker Linux installation](https://docs.docker.com/engine/install/ubuntu/)
- [Docker-compose Linux installation](https://docs.docker.com/compose/install/linux/)

**Windows**

- [Docker Windows installation](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Docker-compose Windows installation](https://docs.docker.com/compose/install/)

### Deployment

After installing Docker and Docker Compose, follow these steps:

1. Clone the repository:
```
git clone https://github.com/CTF-FlagFrenzy/challenges.git
```

2. Navigate to the challenge directory:
```
cd challenges/Pixel_Spy
```

3. Start the Docker container:
```
docker-compose up
```

4. The challenge will be accessible at `http://localhost:80`

You can see all running containers with `docker ps`.

## Customization

To customize the challenge:
- Replace the `hacker.jpg` file with a different image
- Modify the `TEAMKEY` in `docker-compose.yml` to create a unique flag
- Adjust the HTML template for different visual appearances

**HAVE FUN**

> [!NOTE]
> If you have any problems solving this challenge, you can find a full guide in the [writeup.md](./writeup.md) file