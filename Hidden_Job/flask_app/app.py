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

@app.route('/<team_id>')
def team_page(team_id):
    client_ip = request.remote_addr
    logger.info("Index page accessed by IP: %s", client_ip)
    subprocess.run(["python", "flask_app/create_txt.py"])
    challengeflag = os.environ.get("CHALLENGEKEY")
    challengeflag_2 = os.environ.get("CHALLENGEKEY_2")
    teamflag = os.environ.get("TEAMKEY")
    combined_flag = challengeflag + teamflag
    combined_flag_2 = challengeflag_2 + teamflag
#! First flag (index page)
    if combined_flag:
        hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
        logger.info("Flag successfully created and hashed for team %s: %s", team_id, hashed_flag)
    else:
        logger.error(
            "Failed to create flag. Ensure TEAMKEY and CHALLENGEKEY are set in environment variables."
        )
        hashed_flag = "FLAG_NOT_DEFINED"

#! Second flag (robots.txt)
    if combined_flag:
        hashed_flag_2 = "FF{" + hashlib.sha256(combined_flag_2.encode()).hexdigest() + "}"
        logger.info("Flag successfully created and hashed for team %s: %s", team_id, hashed_flag_2)
    else:
        logger.error(
            "Failed to create flag. Ensure TEAMKEY and CHALLENGEKEY are set in environment variables."
        )
        hashed_flag = "FLAG_NOT_DEFINED"

    return f"Welcome to the page for team {team_id}! Your flags are: {hashed_flag} and {hashed_flag_2}"

@app.route('/')
def index():
    team_id = os.getenv('TEAM_ID', 'default_team')
    hashed_team_id = hashlib.sha256(team_id.encode()).hexdigest()
    client_ip = request.remote_addr
    logger.info("Index page accessed by IP: %s", client_ip)
    return redirect(url_for('team_page', team_id=hashed_team_id))

@app.route("/robots.txt")
def hidden_file():
    import os

    return send_from_directory(os.path.join(app.root_path, "hidden"), "robots.txt")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)