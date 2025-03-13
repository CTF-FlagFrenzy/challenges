import hashlib
import os
import shutil
import subprocess

from flask import Flask, send_from_directory

app = Flask(__name__)

original_file = "nice_holiday.JPG"
output_file = "holiday.JPG"
teamflag = os.environ.get("TEAMKEY")


def extract_original_flag(file):
    result = subprocess.run(
        ["exiftool", "-Comment", file], stdout=subprocess.PIPE, text=True, check=True
    )
    exif_data = result.stdout
    for line in exif_data.splitlines():
        if "Comment" in line:
            return line.split(":")[1].strip()
    return None


def embed_combined_flag(file, flag):
    result = subprocess.run(
        ["exiftool", f"-Comment={flag}", file],
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    print(result.stdout)


def copy_file(source, destination):
    shutil.copy(source, destination)


original_flag = extract_original_flag(original_file)

if original_flag:
    print(f"Original-Flag gefunden: {original_flag}")
    combined_flag = original_flag + teamflag
    print(f"Kombinierte Flag: {combined_flag}")
else:
    print("Keine Original-Flag gefunden!")

if combined_flag:
    hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
    print(f"Flag erfolgreich erstellt und gehasht: {hashed_flag}")
    copy_file(original_file, output_file)
    embed_combined_flag(output_file, hashed_flag)
    print(f"Kombinierte, gehashte Flag in {output_file} eingebettet.")
else:
    print(
        "Fehler beim Erstellen der Flag. Stellen Sie sicher, dass TEAMKEY und CHALLENGEKEY in den Umgebungsvariablen festgelegt sind."
    )
    hashed_flag = "FLAG_NOT_DEFINED"


@app.route("/")
def server_image():
    return send_from_directory(".", output_file, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
