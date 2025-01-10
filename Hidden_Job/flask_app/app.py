import os
import hashlib
import logging
import subprocess
from flask import Flask, redirect, url_for, render_template, send_from_directory, request

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    client_ip = request.remote_addr
    logger.info("Index page accessed by IP: %s", client_ip)
    subprocess.run(["python", "flask_app/create_txt.py"])
    # challengeflag = os.environ.get("CHALLENGEKEY")
    # challengeflag_2 = os.environ.get("CHALLENGEKEY_2")
    # teamflag = os.environ.get("TEAMKEY")
    challengeflag = "flag1"
    challengeflag_2 = "flag2"
    teamflag = "flag3"
    combined_flag = challengeflag + teamflag
    combined_flag_2 = challengeflag_2 + teamflag
#! First flag (index page)
    if combined_flag:
        hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
        logger.info(f"Flag successfully created and hashed {hashed_flag}")
    else:
        logger.error("Failed to create flag. Ensure TEAMKEY and CHALLENGEKEY are set in environment variables.")
        hashed_flag = "FLAG_NOT_DEFINED"

#! Second flag (robots.txt)
    if combined_flag:
        hashed_flag_2 = "FF{" + hashlib.sha256(combined_flag_2.encode()).hexdigest() + "}"
        logger.info(f"Flag successfully created and hashed {hashed_flag_2}")
    else:
        logger.error(
            "Failed to create flag. Ensure TEAMKEY and CHALLENGEKEY are set in environment variables."
        )
        hashed_flag = "FLAG_NOT_DEFINED"

    logger.info(f"Your flags are: {hashed_flag} and {hashed_flag_2}")
    return render_template("index.html")

@app.route("/robots.txt")
def hidden_file():
    import os

    return send_from_directory(os.path.join(app.root_path, "hidden"), "robots.txt")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)