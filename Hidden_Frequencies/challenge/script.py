from flask import Flask, send_file

app = Flask(__name__)


@app.route("/")
def download_image():
    return send_file("hidden_frequencies.bmp", as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
