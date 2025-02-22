import subprocess

from flask import Flask, render_template, send_from_directory, redirect

app = Flask(__name__)

@app.route("/")
def index():
    subprocess.run(["python", "flask_app/create_pcap.py"])
    return redirect("/capture.pcap")


@app.route("/capture.pcap")
def capture_file():
    import os
    return send_from_directory(os.path.join(app.root_path, "capture"), "capture.pcap")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
