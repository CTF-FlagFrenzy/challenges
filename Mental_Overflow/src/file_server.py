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


@app.route("/brainfuck.bf")
def serve_brainfuck_file():
    """Endpoint to download the generated brainfuck.bf file"""
    logger.info("Request received for brainfuck.bf download")
    try:
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
            
            # Also check for the file in the current working directory
            cwd_path = os.path.join(os.getcwd(), "download", "brainfuck.bf")
            if os.path.exists(cwd_path):
                logger.info(f"Found file in current working directory: {cwd_path}")
                return send_from_directory(os.path.join(os.getcwd(), "download"), "brainfuck.bf")
            
            return "Brainfuck file not found. Please visit the root page first to generate it.", 404
        
        logger.info(f"Serving file: {file_path}")
        return send_from_directory(DIRECTORY, "brainfuck.bf")
    
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