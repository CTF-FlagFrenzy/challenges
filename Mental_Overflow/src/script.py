import hashlib
import logging
import os
import subprocess
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Generate flag
challengeflag = "CHALLENGEKEY"
teamflag = "TEAMKEY"
combined_flag = challengeflag + teamflag
hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
logger.info(f"Generated hashed flag: {hashed_flag}")

# Generate Brainfuck script
brainfuck_script = ""
line_length = 80  # Maximum length of each line
current_length = 0

for char in hashed_flag:
    ascii_value = ord(char)
    code = "+" * ascii_value + ".>"
    if current_length + len(code) > line_length:
        brainfuck_script += "\n"
        current_length = 0
    brainfuck_script += code
    current_length += len(code)

# Reset pointer
reset_code = "<" * len(hashed_flag)
if current_length + len(reset_code) > line_length:
    brainfuck_script += "\n"
brainfuck_script += reset_code

# Remove the last 5 characters from the Brainfuck script
brainfuck_script = brainfuck_script[:-5]

# Ensure the download directory exists
download_dir = os.path.join("download")
os.makedirs(download_dir, exist_ok=True)

# Save Brainfuck script to a file in the download directory
brainfuck_file_path = os.path.join(download_dir, "brainfuck.bf")
with open(brainfuck_file_path, "w") as bf_file:
    bf_file.write(brainfuck_script)

logger.info(f"Brainfuck script saved to '{brainfuck_file_path}'")

# Start the Flask file server using the same Python interpreter
subprocess.run([sys.executable, "file_server.py"])