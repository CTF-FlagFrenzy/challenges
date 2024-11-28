import logging
import os

from flask import Flask, abort, send_from_directory

app = Flask(__name__)
PORT = 5000
DIRECTORY = os.path.join("download")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@app.route("/brainfuck.bf")
def download_file():
    try:
        return send_from_directory(DIRECTORY, "brainfuck.bf")
    except FileNotFoundError:
        abort(404, description="File not found")


@app.errorhandler(404)
def not_found(error):
    return str(error), 404


if __name__ == "__main__":
    logger.info(f"Serving at port 127.0.0.1:{PORT}")
    app.run(host="0.0.0.0", port=PORT)
