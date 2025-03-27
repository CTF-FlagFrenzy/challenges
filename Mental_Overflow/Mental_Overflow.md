# Mental Overflow Challenge Documentation

## Challenge Overview
Mental Overflow is a Capture The Flag (CTF) challenge designed to test participants' ability to decode obfuscated data through multiple layers of encoding. The challenge involves a web server that generates and serves a Base64-encoded Brainfuck program. When executed, the program reveals an obfuscated flag.

---

## Technical Implementation

### Architecture
The challenge is built using a Flask-based web server running inside a Docker container. The main components are:

1. **Web Server** (`file_server.py`): A Flask application that serves the challenge file.
2. **Flag Generator** (`script.py`): A Python script that generates the encoded flag.
3. **Containerization** (`Dockerfile` and `docker-compose.yml`): Configuration for deployment.

---

### Web Server Component

The Flask server (`file_server.py`) provides two main endpoints:

- **`/`**: Triggers the flag generation script and redirects to the download endpoint.
- **`/challenge.bin`**: Serves the encoded challenge file.

#### Key Code Snippets

**Flask Endpoint for Root (`/`)**
```python
# filepath: c:\Users\manag\Documents\GitHub\challenges\Mental_Overflow\src\file_server.py
@app.route("/")
def index():
    """Root page that triggers script execution and redirects to download page"""
    logger.info("Request received at root, triggering script execution")
    try:
        result = subprocess.run(
            ["python", SCRIPT_PATH], 
            capture_output=True, 
            text=True, 
            env=dict(os.environ, **{"DOWNLOAD_DIR": DIRECTORY})
        )
        if result.returncode != 0:
            logger.error(f"Script execution failed: {result.stderr}")
            return "Script execution failed. Please check server logs.", 500
        return redirect(url_for('serve_brainfuck_file'))
    except Exception as e:
        logger.exception(f"Error in index: {str(e)}")
        return "An error occurred. Please check server logs.", 500
```

**Flask Endpoint for File Download (`/challenge.bin`)**
```python
# filepath: c:\Users\manag\Documents\GitHub\challenges\Mental_Overflow\src\file_server.py
@app.route("/challenge.bin")
def serve_brainfuck_file():
    """Endpoint to download the generated challenge.bin file"""
    file_path = os.path.join(DIRECTORY, "challenge.bin")
    if os.path.exists(file_path):
        return send_from_directory(DIRECTORY, "challenge.bin")
    return "Brainfuck file not found. Please visit the root page first to generate it.", 404
```

---

### Flag Generation

The flag generation logic is implemented in `script.py`. It combines a fixed challenge component with a team-specific key, hashes the result, and encodes it into a Brainfuck program.

#### Key Steps in Flag Generation

1. **Combine Challenge and Team Key**
   ```python
   challengeflag = "#8W@3fp5#Y"
   teamflag = os.environ.get("TEAMKEY")
   combined_flag = challengeflag + teamflag
   hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
   ```

2. **Obfuscate the Flag**
   Replace curly braces with random characters:
   ```python
   random_chars = random.sample(string.ascii_letters + string.digits + "!@#$%^&*()", 2)
   brainfuck_flag = hashed_flag.replace("{", random_chars[0]).replace("}", random_chars[1])
   ```

3. **Generate Brainfuck Code**
   Convert the obfuscated flag into Brainfuck instructions:
   ```python
   brainfuck_script = ""
   for char in brainfuck_flag:
       brainfuck_script += "+" * ord(char) + ".>"
   brainfuck_script += "<" * len(brainfuck_flag)  # Reset pointer
   ```

4. **Base64 Encode the Brainfuck Script**
   ```python
   encrypted_brainfuck_script = base64.b64encode(brainfuck_script.encode('utf-8')).decode('utf-8')
   ```

5. **Save the Encoded Script**
   ```python
   with open(brainfuck_file_path, "w") as bf_file:
       bf_file.write(encrypted_brainfuck_script)
   ```

---

### Deployment

The application is containerized using Docker. The `Dockerfile` and `docker-compose.yml` files define the environment and service configuration.

#### Dockerfile
```dockerfile
# filepath: c:\Users\manag\Documents\GitHub\challenges\Mental_Overflow\src\Dockerfile
FROM python:3
COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /code
WORKDIR /code
EXPOSE 80
ENTRYPOINT ["python", "src/file_server.py"]
```

#### Docker Compose
```yml
# filepath: c:\Users\manag\Documents\GitHub\challenges\Mental_Overflow\docker-compose.yml
version: '3'
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

---

## Challenge Solution Flow

1. **Access the Web Server**: Visit the root endpoint (`/`) to trigger flag generation.
2. **Download the File**: Redirect to `/challenge.bin` to download the Base64-encoded Brainfuck program.
3. **Decode the File**: Use a Base64 decoder to extract the Brainfuck code.
4. **Execute the Brainfuck Code**: Use a Brainfuck interpreter to reveal the obfuscated flag.
5. **Reformat the Flag**: Replace random characters with curly braces to get the final flag.
6. **Submit the Flag**: Submit the flag in the format `FF{...}`.

---

## Security Considerations

- **Environment Variables**: The `TEAMKEY` environment variable must be securely managed to prevent flag leakage.
- **Server Logs**: Logs contain sensitive information (e.g., generated flags) and should not be exposed to participants.
- **Container Isolation**: The challenge is designed to run in an isolated Docker environment to prevent unauthorized access.

---

## Testing

The challenge includes detailed test cases in `test_Mental_Overflow.md`. Key tests include:

1. **Deployment Verification**: Ensure the Docker container starts correctly.
2. **File Generation**: Verify that `challenge.bin` is generated and contains valid Base64-encoded Brainfuck code.
3. **Service Accessibility**: Test that the endpoints are accessible and functional.
4. **Flag Validation**: Confirm that the generated flag matches the expected format.

---

## Example Walkthrough

1. **Download the File**
   ```bash
   curl -O http://localhost/challenge.bin
   ```

2. **Decode the Base64 Content**
   ```bash
   base64 -d challenge.bin > decoded.bf
   ```

3. **Execute the Brainfuck Code**
   ```bash
   bf decoded.bf
   ```

4. **Extract and Format the Flag**
   Replace random characters with curly braces to get the final flag:
   ```
   FF{...}
   ```

5. **Submit the Flag**: Enter the flag into the scoring system to complete the challenge.