# Mental Overflow Challenge Documentation

## Challenge Overview
Mental Overflow is a Capture The Flag (CTF) challenge designed to test participants' ability to decode obfuscated data through multiple layers of encoding. The challenge involves a web server that generates and serves a Base64-encoded BF program. When executed, the program reveals an obfuscated flag.

## Technical Implementation

### Architecture
The challenge uses a microservice architecture built with the following components:

1. **Web Server** (`file_server.py`): A Flask application that serves the challenge file.
2. **Flag Generator** (`script.py`): A Python script that generates the encoded flag.
3. **Containerization** (`Dockerfile` and `docker-compose.yml`): Configuration for deployment and isolation.

### Component 1: Web Server (`file_server.py`)

This is the main entry point for the challenge. It's a Flask web application that:
- Serves the root endpoint to trigger flag generation
- Provides a download endpoint for the encoded challenge file
- Handles error conditions and logging

#### Full Source Code:

```python
import logging
import os
import subprocess
import time

from flask import Flask, abort, send_from_directory, redirect, url_for

app = Flask(__name__)

# Use absolute paths based on the script's location for container compatibility
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)  # Go up one level from src to project root
DIRECTORY = os.path.join(PROJECT_ROOT, "download")  # Create download folder outside src
SCRIPT_PATH = os.path.join(CURRENT_DIR, "script.py")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Ensure download directory exists
os.makedirs(DIRECTORY, exist_ok=True)
logger.info(f"Download directory created at: {DIRECTORY}")


@app.route("/")
def index():
    """Root page that triggers script execution and redirects to download page"""
    logger.info("Request received at root, triggering script execution")
    try:
        # Execute script to ensure file is generated
        logger.info(f"Executing script at: {SCRIPT_PATH}")
        result = subprocess.run(
            ["python", SCRIPT_PATH], 
            capture_output=True, 
            text=True, 
            check=False,
            env=dict(os.environ, **{"DOWNLOAD_DIR": DIRECTORY})
        )
        
        if result.returncode != 0:
            logger.error(f"Script execution failed: {result.stderr}")
            return "Script execution failed. Please check server logs.", 500
        else:
            logger.info("Script executed successfully")
            # Give a short delay to ensure file is written completely
            time.sleep(0.5)
            # Redirect to the download endpoint
            return redirect(url_for('serve_brainfuck_file'))
    
    except Exception as e:
        logger.exception(f"Error in index: {str(e)}")
        return "An error occurred. Please check server logs.", 500


@app.route("/challenge.bin")
def serve_brainfuck_file():
    """Endpoint to download the generated challenge.bin file"""
    logger.info("Request received for challenge.bin download")
    try:
        # Verify the file exists before attempting to serve it
        file_path = os.path.join(DIRECTORY, "challenge.bin")
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            
            # Try to locate the file in the current directory structure
            for root, _, files in os.walk(PROJECT_ROOT):
                if "challenge.bin" in files:
                    alternate_path = os.path.join(root, "challenge.bin")
                    logger.info(f"Found alternate file location: {alternate_path}")
                    return send_from_directory(root, "challenge.bin")
            
            # Also check for the file in the current working directory
            cwd_path = os.path.join(os.getcwd(), "download", "challenge.bin")
            if os.path.exists(cwd_path):
                logger.info(f"Found file in current working directory: {cwd_path}")
                return send_from_directory(os.path.join(os.getcwd(), "download"), "challenge.bin")
            
            return "File not found. Please visit the root page first to generate it.", 404
        
        logger.info(f"Serving file: {file_path}")
        return send_from_directory(DIRECTORY, "challenge.bin")
    
    except Exception as e:
        logger.exception(f"Error in serve_brainfuck_file: {str(e)}")
        return "An error occurred while attempting to serve the file.", 500


@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 error: {str(error)}")
    return str(error), 404


@app.errorhandler(500)
def server_error(error):
    logger.error(f"500 error: {str(error)}")
    return str(error), 500


if __name__ == "__main__":
    logger.info(f"Starting server on 0.0.0.0:80, serving files from {DIRECTORY}")
    app.run(host="0.0.0.0", port=80)
```

#### Key Features:

1. **Path Configuration**
   - Uses absolute paths to ensure compatibility across different environments
   - Creates a download directory for generated files

2. **Logging**
   - Comprehensive logging with timestamps and log levels
   - Captures important events and errors for debugging

3. **Root Endpoint (`/`)**
   - Executes the flag generation script
   - Passes necessary environment variables
   - Redirects to the download endpoint upon success
   - Includes error handling and appropriate HTTP status codes

4. **Download Endpoint (`/challenge.bin`)**
   - Serves the generated challenge file
   - Implements multiple fallback mechanisms to locate the file
   - Returns appropriate error messages if the file isn't found

5. **Error Handlers**
   - Custom handlers for 404 (Not Found) and 500 (Server Error) responses
   - Logs error details for troubleshooting

### Component 2: Flag Generator (`script.py`)

This script is responsible for:
- Generating a unique flag based on a fixed challenge string and team-specific key
- Obfuscating the flag by replacing key characters
- Converting the flag to an esoteric programming language (BF)
- Encoding the result with Base64

#### Full Source Code:

```python
import hashlib
import logging
import os
import random
import string
import base64

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Generate flag
challengeflag = "#8W@3fp5#Y"
teamflag = os.environ.get("TEAMKEY")
combined_flag = challengeflag + teamflag
hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
logger.info(f"Generated hashed flag: {hashed_flag}")

# Create a modified version of the flag with random characters instead of curly braces
random_chars = [
    f'"{char}"'
    for char in random.sample(string.ascii_letters + string.digits + "!@#$%^&*()", 2)
]
brainfuck_flag = hashed_flag.replace("{", random_chars[0]).replace("}", random_chars[1])
logger.info(f"Modified flag for BF script: {brainfuck_flag}")

# Generate BF script
brainfuck_script = ""
line_length = 80  # Maximum length of each line
current_length = 0

for char in brainfuck_flag:
    ascii_value = ord(char)
    code = "+" * ascii_value + ".>"
    if current_length + len(code) > line_length:
        brainfuck_script += "\n"
        current_length = 0
    brainfuck_script += code
    current_length += len(code

# Reset pointer
reset_code = "<" * len(brainfuck_flag)
if current_length + len(reset_code) > line_length:
    brainfuck_script += "\n"
brainfuck_script += reset_code

# Encrypt the BF script with Base64
brainfuck_script_bytes = brainfuck_script.encode('utf-8')
encrypted_brainfuck_script = base64.b64encode(brainfuck_script_bytes).decode('utf-8')
logger.info("BF script encrypted with Base64")

# Ensure the download directory exists
download_dir = os.environ.get("DOWNLOAD_DIR", os.path.join("download"))
os.makedirs(download_dir, exist_ok=True)

# Save encrypted BF script to a file in the download directory
brainfuck_file_path = os.path.join(download_dir, "challenge.bin")
with open(brainfuck_file_path, "w") as bf_file:
    bf_file.write(encrypted_brainfuck_script)

logger.info(f"Base64 encrypted BF script saved to '{brainfuck_file_path}'")
```

#### Key Algorithms:

1. **Flag Generation**
   - Combines a fixed challenge string (`#8W@3fp5#Y`) with a team-specific key
   - Applies SHA-256 hashing to create a unique flag
   - Formats it with the "FF{...}" prefix

2. **Flag Obfuscation**
   - Selects two random characters from a set of alphanumeric and special characters
   - Replaces the curly braces in the flag with these random characters
   - Adds quotation marks around the replacement characters

3. **BF Code Generation**
   - For each character in the obfuscated flag:
     - Creates a sequence of plus signs (`+`) corresponding to the ASCII value
     - Outputs the character with a dot (`.`)
     - Moves to the next cell with a greater-than sign (`>`)
   - Adds a reset sequence of less-than signs (`<`) to return to the start

4. **Encoding and Storage**
   - Encodes the BF code with Base64
   - Saves the encoded content to a file named "challenge.bin"

### Component 3: Containerization

The application is containerized using Docker for easy deployment and isolation.

#### Dockerfile:

```dockerfile
FROM python:3

# Copy requirements and install dependencies
COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire codebase into the container
COPY . /code
WORKDIR /code
EXPOSE 80
# Ensure the script is executable
RUN chmod +x src/script.py

# Set the entrypoint to run file_server.py
ENTRYPOINT ["python", "src/file_server.py"]
```

#### Docker Compose:

```yml
version: '3'

volumes:
  my-django-data:

services:
  flask:
    build:
      context: .
      dockerfile: src/Dockerfile

    ports:
      - '80:80'

    environment:
      - TEAMKEY=XXXXXXX
```

#### Container Design:

1. **Base Image**
   - Uses Python 3 as the foundation
   - Provides a consistent runtime environment

2. **Dependencies**
   - Installs required packages from requirements.txt:
     - Flask 2.0.2
     - Werkzeug 2.0.2

3. **File Structure**
   - Copies the application code to `/code` in the container
   - Sets `/code` as the working directory

4. **Networking**
   - Exposes port 80 for web traffic

5. **Environment Variables**
   - TEAMKEY: Team-specific key used in flag generation
   - Can be customized for each deployment

6. **Startup**
   - Launches the Flask web server as the container's main process

**HAVE FUN**

> [!NOTE]
> If you have any problems solving this challenge, you can find a detailed writeup [here](https://github.com/CTF-FlagFrenzy/challenges/blob/main/Mental_Overflow/writeup.md)