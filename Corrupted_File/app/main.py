import hashlib
import os
import tarfile

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse

if os.environ.get("TEAMKEY") is None:
    load_dotenv()

debug = os.getenv("DEBUG", "False") == "True"
print(debug)

team_key = os.getenv("TEAMKEY")
challenge_key = os.getenv("CHALLENGE")
combined_flag = challenge_key + team_key
hashed_flag = f"FF{{{hashlib.md5(combined_flag.encode()).hexdigest()}}}"
if debug:
    print(f"Team Key: {team_key}")
    print(f"Challenge Key: {challenge_key}")
    print(f"Flag: {hashed_flag}")

# create a text file with the flag
with open("flag.txt", "w") as f:
    f.write(hashed_flag)

# compress the file to a tar.gz file
with tarfile.open("document", "w:gz") as tar:
    tar.add("flag.txt")

# replace the first two bytes from the archive from 0x1f 0x8b to 0x00 0x00 to hide the file type
# makes it practically impossible without altering the bytes back
with open("document", "r+b") as f:
    f.seek(0)  # Move to the beginning of the file
    f.write(b"\x00\x00")  # Write the new bytes


app = FastAPI()


@app.get("/")
def read_root():
    file_path = "document"
    # send some additional headers because firefox can't be normal
    headers = {"Content-Disposition": 'attachment; filename="document"'}
    return FileResponse(file_path, headers=headers)
