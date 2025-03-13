import hashlib
import logging
import os
import random
import string
import base64

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Generate flag
challengeflag = "#8W@3fp5#Y"
teamflag = os.environ.get("TEAMKEY")
combined_flag = challengeflag + teamflag
hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
logger.info(f"Generated hashed flag: {hashed_flag}")

# Create a modified version of the flag with random characters instead of curly braces
random_chars = [
    f'"{char}"'
    for char in random.sample(string.ascii_letters + string.digits + "!@#$%^&*()", 2)
]
brainfuck_flag = hashed_flag.replace("{", random_chars[0]).replace("}", random_chars[1])
logger.info(f"Modified flag for Brainfuck script: {brainfuck_flag}")

# Generate Brainfuck script
brainfuck_script = ""
line_length = 80  # Maximum length of each line
current_length = 0

for char in brainfuck_flag:
    ascii_value = ord(char)
    code = "+" * ascii_value + ".>"
    if current_length + len(code) > line_length:
        brainfuck_script += "\n"
        current_length = 0
    brainfuck_script += code
    current_length += len(code)

# Reset pointer
reset_code = "<" * len(brainfuck_flag)
if current_length + len(reset_code) > line_length:
    brainfuck_script += "\n"
brainfuck_script += reset_code

# Encrypt the Brainfuck script with Base64
brainfuck_script_bytes = brainfuck_script.encode('utf-8')
encrypted_brainfuck_script = base64.b64encode(brainfuck_script_bytes).decode('utf-8')
logger.info("Brainfuck script encrypted with Base64")

# Ensure the download directory exists
download_dir = os.environ.get("DOWNLOAD_DIR", os.path.join("download"))
os.makedirs(download_dir, exist_ok=True)

# Save encrypted Brainfuck script to a file in the download directory
brainfuck_file_path = os.path.join(download_dir, "challenge.bin")
with open(brainfuck_file_path, "w") as bf_file:
    bf_file.write(encrypted_brainfuck_script)

logger.info(f"Base64 encrypted Brainfuck script saved to '{brainfuck_file_path}'")