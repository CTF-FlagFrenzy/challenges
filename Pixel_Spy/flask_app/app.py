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
