import logging
import os
import subprocess

from flask import Flask, abort, send_from_directory

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
def serve_brainfuck_file():
    logger.info("Request received for brainfuck.bf")
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
            abort(500, description="Internal server error")
        else:
            logger.info("Script executed successfully")
        
        # Verify the file exists before attempting to serve it
        file_path = os.path.join(DIRECTORY, "brainfuck.bf")
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            
            # Try to locate the file in the current directory structure
            for root, _, files in os.walk(PROJECT_ROOT):
                if "brainfuck.bf" in files:
                    alternate_path = os.path.join(root, "brainfuck.bf")
                    logger.info(f"Found alternate file location: {alternate_path}")
                    return send_from_directory(root, "brainfuck.bf")
            
            abort(404, description="File not found")
        
        logger.info(f"Serving file: {file_path}")
        return send_from_directory(DIRECTORY, "brainfuck.bf")
    except Exception as e:
        logger.exception(f"Error in serve_brainfuck_file: {str(e)}")
        abort(500, description="Internal server error")


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