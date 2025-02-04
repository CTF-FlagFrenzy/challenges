import hashlib
import logging
import os
import subprocess

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)

app = Flask(__name__)
app.secret_key = os.urandom(24)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
combined_flag = ""


@app.route("/")
def index():
    client_ip = request.remote_addr
    logger.info("Index page accessed by IP: %s", client_ip)
    subprocess.run(["python", "flask_app/create_txt.py"])
    challengeflag = os.environ.get("CHALLENGEKEY")
    teamflag = os.environ.get("TEAMKEY")
    combined_flag = challengeflag + teamflag
    if combined_flag:
        hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
        logger.info(f"Flag successfully created and hashed {hashed_flag}")
    else:
        logger.error(
            "Failed to create flag. Ensure TEAMKEY and CHALLENGEKEY are set in environment variables."
        )
        hashed_flag = "FLAG_NOT_DEFINED"
    return render_template(
        "index.html", logged_in=session.get("logged_in"), hashed_flag=hashed_flag
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "Admin" and password == "N3tzw3rkTechNik":
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            return "Invalid credentials", 401
    return render_template("index.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("index"))


@app.route("/download/ProjectDelta.zip")
def download_project_delta():
    return send_from_directory(
        os.path.join(app.root_path, "download"), "ProjectDelta.zip"
    )


@app.route("/<combined_flag>/robots.txt")
def hidden_file(combined_flag):
    return send_from_directory(os.path.join(app.root_path, "hidden"), "robots.txt")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
