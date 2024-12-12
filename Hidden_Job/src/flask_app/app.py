import os
import hashlib
import logging
from flask import Flask, redirect, url_for

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

@app.route('/<team_id>')
def team_page(team_id):
    challengeflag = os.environ.get("CHALLENGEKEY")
    teamflag = os.environ.get("TEAMKEY")
    combined_flag = challengeflag + teamflag + team_id

    if combined_flag:
        hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
        logger.info("Flag successfully created and hashed for team %s: %s", team_id, hashed_flag)
    else:
        logger.error(
            "Failed to create flag. Ensure TEAMKEY and CHALLENGEKEY are set in environment variables."
        )
        hashed_flag = "FLAG_NOT_DEFINED"
    return f"Welcome to the page for team {team_id}! Your flag is: {hashed_flag}"

@app.route('/')
def index():
    team_id = os.getenv('TEAM_ID', 'default_team')
    return redirect(url_for('team_page', team_id=team_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)