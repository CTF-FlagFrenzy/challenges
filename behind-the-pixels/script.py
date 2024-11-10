import subprocess
import shutil
from flask import Flask, send_from_directory

app = Flask(__name__)

original_file = "nice_holiday.JPG"
global_flag = "ABCD"
output_file = "nice_holiday_copy.JPG"

def extract_original_flag(file):
    result = subprocess.run(["exiftool", "-Comment", file], stdout=subprocess.PIPE, text=True, check=True)
    exif_data = result.stdout
    for line in exif_data.splitlines():
        if "Comment" in line:
            return line.split(":")[1].strip()
    return None

def embed_combined_flag(file, flag):
    result = subprocess.run(["exiftool", f"-Comment={flag}", file], stdout=subprocess.PIPE, text=True, check=True)
    print(result.stdout)

def copy_file(source, destination):
    shutil.copy(source, destination)

original_flag = extract_original_flag(original_file)

if original_flag:
    print(f"Original-Flag gefunden: {original_flag}")
    combined_flag = global_flag + original_flag
    print(f"Kombinierte Flag: {combined_flag}")
    copy_file(original_file, output_file)
    embed_combined_flag(output_file, combined_flag)
    print(f"Kombinierte Flag in {output_file} eingebettet.")
else:
    print("Keine Original-Flag gefunden!")

@app.route('/image')
def server_image():
    return send_from_directory('.', output_file)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
