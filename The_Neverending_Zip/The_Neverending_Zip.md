# The Neverending Zip Challenge - Technical Documentation

## Overview

The Neverending Zip is a CTF (Capture The Flag) challenge that tests participants' ability to automate the extraction of deeply nested ZIP files. This document provides technical details about the implementation and architecture of the challenge.

## System Architecture

The challenge consists of:
1. A Flask web application
2. A ZIP file generation script
3. A containerized deployment environment

The application is containerized using Docker and deployed using Docker Compose, making it portable and easy to deploy consistently across different environments.

## Components

### 1. Flask Web Application (`flask_app/app.py`)

The Flask application serves as the user interface and backend for the challenge. It handles:

- Presenting a web interface to users
- Managing the ZIP file creation process
- Providing real-time progress updates
- Serving the generated ZIP file for download

Key features of the Flask application:

#### Status Management

The application uses a status file to track the progress of ZIP creation:

```python
# Status file path
status_file_path = os.path.join(tempfile.gettempdir(), "zip_creation_status.json")

def read_status_file():
    if os.path.exists(status_file_path):
        try:
            with open(status_file_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    return None
```

#### ZIP File Creation

ZIP file creation is managed by a separate process:

```python
def create_zip_file():
    global zip_creation_in_progress, zip_creation_complete, zip_creation_start_time, estimated_total_time
    zip_creation_in_progress = True
    zip_creation_complete = False
    zip_creation_start_time = time.time()

    # Create status file
    with open(status_file_path, "w") as f:
        json.dump(
            {
                "start_time": zip_creation_start_time,
                "estimated_total_time": estimated_total_time,
                "progress": 0.0,
            },
            f,
        )

    # Start ZIP creation process and pass status file
    subprocess.run(["python", "flask_app/create_zip.py", "--status-file", status_file_path])

    zip_creation_in_progress = False
    zip_creation_complete = True
```

#### Real-time Progress Updates via Server-Sent Events (SSE)

The application uses SSE to provide real-time updates about ZIP creation progress:

```python
@app.route("/stream")
def stream():
    def generate():
        global zip_creation_start_time

        while True:
            zip_path = os.path.join(app.root_path, "zip", "HaveFun.zip")

            if os.path.exists(zip_path) or zip_creation_complete:
                data = {"ready": True, "progress": 1.0, "est_time_remaining": 0}
                yield f"data: {json.dumps(data)}\n\n"
                break  # End the stream

            # Read status from file
            status = read_status_file()
            if status and "progress" in status:
                # Process status information and send it to the client
                # ...

            time.sleep(1)  # Update rate

    return Response(generate(), mimetype="text/event-stream")
```

### 2. ZIP File Generator (`flask_app/create_zip.py`)

The ZIP file generator is responsible for creating the deeply nested ZIP structure that forms the core challenge:

#### Flag Generation

The flag is dynamically generated based on a challenge key and a team key:

```python
challengekey = "M5OQXpXsE^Us"
teamkey = os.environ.get("TEAMKEY")
if not teamkey:
    logger.warning("TEAMKEY environment variable not set, using default")
    teamkey = "default_key"

combined_flag = challengekey + teamkey
hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
```

#### ZIP Creation Process

The script creates a deeply nested ZIP structure with approximately 11,111 layers:

```python
current_zip = inner_zip_path
max_layers = 11111
batch_size = 1000

for layer in range(1, max_layers + 1):
    prev_zip = current_zip
    current_zip = os.path.join(temp_dir, f"temp_layer_{layer}.zip")
    
    # Simple zip creation - always use the same name for the inner zip
    with zipfile.ZipFile(
        current_zip, "w", compression=zipfile.ZIP_DEFLATED
    ) as zipf:
        zipf.write(prev_zip, arcname=zip_filename)

    # Delete the previous zip to save space
    os.remove(prev_zip)
```

#### Performance Monitoring and Status Updates

The script tracks performance metrics and updates the status file:

```python
if layer % batch_size == 0:
    # Display performance metrics every batch_size layers
    current_time = time.time()
    elapsed = current_time - start_time
    layers_per_second = layer / elapsed if elapsed > 0 else 0
    estimated_total = max_layers / layers_per_second if layers_per_second > 0 else 0
    remaining = estimated_total - elapsed

    # Update status file
    if status_file and os.path.exists(os.path.dirname(status_file)):
        try:
            with open(status_file, "w") as f:
                json.dump(
                    {
                        "start_time": start_time,
                        "current_time": current_time,
                        "progress": layer / max_layers,
                        "estimated_total_time": estimated_total,
                        "remaining_time": remaining,
                        "layers_per_second": layers_per_second,
                    },
                    f,
                )
        except Exception as e:
            logger.error(f"Error updating status file: {e}")
```

### 3. Web Interface (`flask_app/templates/index.html`)

The web interface provides users with:
- Information about the challenge
- Real-time progress updates during ZIP creation
- A download button when the ZIP is ready

#### Progress Bar and Status Updates

The interface uses JavaScript to update a progress bar and show status information:

```javascript
eventSource.onmessage = function(event) {
    try {
        const data = JSON.parse(event.data);
        
        if (data.ready) {
            // Enable download button and update status
            const downloadBtn = document.getElementById('download-link');
            downloadBtn.href = '/flag.zip';
            downloadBtn.classList.remove('disabled');
            downloadBtn.innerText = 'Download Challenge';
            
            // Update status message
            document.getElementById('status-message').innerHTML = 'Zip file is ready!';
            
            // Update progress bar to 100%
            const progressBar = document.getElementById('progress-bar');
            progressBar.style.width = '100%';
            progressBar.innerText = '100%';
            
            // Auto download
            window.location.href = '/flag.zip';
            
            // Close the event source
            eventSource.close();
        } else {
            // Update progress bar
            if (data.progress !== undefined) {
                const progressBar = document.getElementById('progress-bar');
                const progress = Math.round(data.progress * 100);
                progressBar.style.width = progress + '%';
                progressBar.innerText = progress + '%';
                
                // Update estimated time remaining
                if (data.est_time_remaining !== undefined) {
                    // Format and display time remaining
                    // ...
                }
            }
        }
    } catch (e) {
        console.error("Error processing server message:", e);
    }
}
```

### 4. Container Configuration (`docker-compose.yml` and `flask_app/Dockerfile`)

The challenge is containerized using Docker, with configuration defined in `docker-compose.yml`:

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

The `TEAMKEY` environment variable allows customization of the generated flag, making it possible to create unique flags for different teams or instances of the challenge.

### 5. Extraction Helper Script (`flask_app/unzip.py`)

This utility script demonstrates a proper approach for extracting the nested ZIP structure:

```python
def extract_nested_zips(zip_path, extract_dir):
    """Recursively extract nested zip files until we find the flag."""
    # Create extract directory if it doesn't exist
    os.makedirs(extract_dir, exist_ok=True)

    # Stats tracking
    start_time = time.time()
    layer_count = 0
    last_report_time = start_time
    report_interval = 5  # Report progress every 5 seconds

    current_zip = zip_path

    try:
        while True:
            layer_count += 1
            current_extract_dir = os.path.join(extract_dir, f"layer_{layer_count}")
            os.makedirs(current_extract_dir, exist_ok=True)

            # Extract the current zip
            with zipfile.ZipFile(current_zip, "r") as zipf:
                zipf.extractall(current_extract_dir)

                # Check if we found the flag
                if "flag.txt" in zipf.namelist():
                    flag_path = os.path.join(current_extract_dir, "flag.txt")
                    logger.info(f"Found flag file at layer {layer_count}!")
                    with open(flag_path, "r") as f:
                        flag_content = f.read()
                        logger.info(f"Flag content:\n{flag_content}")
                    break

                # Find the next zip file
                next_zip = None
                for item in zipf.namelist():
                    if item.lower().endswith(".zip"):
                        next_zip = os.path.join(current_extract_dir, item)
                        break

                if next_zip is None:
                    logger.error("No zip file found in layer. Extraction complete but no flag found.")
                    break

                current_zip = next_zip
```

## Technical Challenges and Solutions

### 1. Managing Memory Usage

Creating and extracting deeply nested ZIP files could potentially consume excessive memory. Solutions implemented:

- **During Creation**: The script deletes each previous ZIP layer after it's been incorporated into the next layer, maintaining a small memory footprint.
  
- **During Extraction**: The helper script can be configured to remove previous extraction layers as it progresses, preventing disk space exhaustion.

### 2. Real-time Progress Updates

Providing accurate progress updates for a process that may run for 15+ minutes is challenging:

- **Server-Sent Events**: Used instead of WebSockets for simplicity and reliability
- **Status File**: Shared between the web app and ZIP creation script
- **Performance Metrics**: Calculation of layers per second and time remaining

### 3. Docker Containerization

Containerization ensures consistent behavior across environments:

- **Environment Variables**: Used for configurable elements like team keys
- **Port Mapping**: Exposing port 80 for easy web access
- **Resource Limits**: Can be applied to prevent resource exhaustion

## Security Considerations

1. **Input Validation**: All user inputs are validated to prevent injection attacks
2. **Resource Limitations**: The application includes timeouts and limits to prevent DoS attacks
3. **Safe File Handling**: All file operations use secure practices to prevent directory traversal
4. **Containerization**: Isolates the application from the host system

## Conclusion

The Neverending Zip challenge demonstrates the importance of automation in dealing with repetitive tasks. By creating a deeply nested ZIP structure that would be practically impossible to navigate manually, it forces participants to develop programmatic solutions.

The challenge balances technical complexity with educational value, teaching concepts related to:

- File compression and extraction
- Process automation
- Real-time status reporting
- Resource management
- Web application development
