import hashlib
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse

if os.environ.get("TEAMKEY") is None:
    load_dotenv()

debug = os.getenv("DEBUG", "False") == "True"
#! COMMENT THIS OUT
#! COMMENT THIS OUT
#! COMMENT THIS OUT
debug = True

print(debug)

team_key = os.getenv("TEAMKEY")
challenge_key = "k^kpB2Y99nKwhjex8!G1Mpw7cb!gEMtfa@kuPj*dzn%yqu65P^6RhnPtUZsQF0g&"
combined_flag = challenge_key + team_key
hashed_flag = f"FF{{{hashlib.md5(combined_flag.encode()).hexdigest()}}}"
if debug:
    print(f"Team Key: {team_key}")
    print(f"Challenge Key: {challenge_key}")
    print(f"Flag: {hashed_flag}")
mask = "What might this string be doing?????"
# convert the mask and hashed_flag to binary for debugging purposes
binary_mask = " ".join(format(ord(c), "b") for c in mask)
binary_hashed_flag = " ".join(format(ord(c), "b") for c in hashed_flag)


def xor_strings(s1, s2):
    # Ensure the strings are of the same length
    if len(s1) != len(s2):
        raise ValueError("Strings must be of the same length")

    # Convert strings to binary and XOR them
    xor_result = "".join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

    return xor_result


masked_string = xor_strings(mask, hashed_flag)

if debug:
    debug_message = f"""
//////////////DEBUG///////////////
Mask: {mask}
Mask Length: {len(mask)}
Binary Mask: {binary_mask}
--------------------------------
Flag: {hashed_flag}
Flag Length: {len(hashed_flag)}
Binary Flag: {binary_hashed_flag}
--------------------------------
Masked String: {masked_string}
Masked String Length: {len(masked_string)}
Binary Masked String: {' '.join(format(ord(c), 'b') for c in masked_string)}
//////////////DEBUG///////////////
"""
    print(debug_message)
    with open("debug.txt", "w") as f:
        f.write(debug_message)

# write the data to a file that FastAPI can server
with open("encoded.txt", "w") as f:
    f.write(masked_string)
    f.write(mask)

app = FastAPI()


@app.get("/")
def read_root():
    return FileResponse("encoded.txt")

if debug:
    @app.get("/debug")
    def read_debug():
        return FileResponse("debug.txt")
