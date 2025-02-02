# Binary Puzzeling

A crypto challenge with the goal to decipher a string with the provided key
**Level**: Medium



## Challenge Overview:

The user gets a string and has to figure out how this string was encoded and then reverse the encoding. The encoding used is xor.
---

### Dockerfile

The `Dockerfile` just installs a python 3.9 environment and adds the dependencies from requirements.txt. The dependencies inlcude mostly things for FastAPI, that is used to present the string to the user.
```yml
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

### Python script

The `main.py` includes all the code necessary for running this challenge. It consists of two parts, the challenge string generation and the FastAPI service. 
For encoding the string a function called `xor_strings(string1, string2)` is used. It converts the strings to binary, does an XOR operation and converts the result back into a string. The resulting string will often look nonsensical, as it is out of bounds of the usual unicode characters: 
```
.CA	YV
AAF_YJK@FXVSDSA]
V_

	
```
The code contains some debug information that can be used to solve the challenge if it is to hard by setting an environment variable "Debug" to "True".

```python
import hashlib
import os
import random

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
if(debug):
    print(f"Team Key: {team_key}")
    print(f"Challenge Key: {challenge_key}")
    print(f"Flag: {hashed_flag}")
mask = "What might this string be doing?????"
#convert the mask and hashed_flag to binary for debugging purposes
binary_mask = ' '.join(format(ord(c), 'b') for c in mask)
binary_hashed_flag = ' '.join(format(ord(c), 'b') for c in hashed_flag)




def xor_strings(s1, s2):
    # Ensure the strings are of the same length
    if len(s1) != len(s2):
        raise ValueError("Strings must be of the same length")
    
    # Convert strings to binary and XOR them
    xor_result = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))
    
    return xor_result

masked_string = xor_strings(mask, hashed_flag)

if(debug):
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

#write the data to a file that FastAPI can server
with open("encoded.txt", "w") as f:
    f.write(masked_string)
    f.write(mask)

app = FastAPI()


@app.get("/")
def read_root():
    return FileResponse("encoded.txt")

```


## Technical guideline

### Installation

> [!NOTE]
> Make sure to install docker and docker-compose first

**Linux**

- [Docker Linux installation](https://docs.docker.com/engine/install/ubuntu/)

- [Docker-compose Linux installation](https://docs.docker.com/compose/install/linux/)

**Windwos**

- [Docker Windows installation](https://docs.docker.com/desktop/setup/install/windows-install/)

- [Docker-compose Windows installation](https://docs.docker.com/compose/install/)

After you installed docker and docker-compose you need to pull the repository via cli using this command.

```
git pull https://github.com/CTF-FlagFrenzy/challenges.git
```

Then you navigate to the root of the `Binary_Puzzeling` challenge and type the following command in the cli.

```
docker-compose up
```

You can see all running container with `docker ps`.

**HAVE FUN**

> [!NOTE]
> If you have any problems solving this challenge you can find a full guide [here](https://github.com/CTF-FlagFrenzy/challenges/blob/main/Binary_Puzzeling/writeup.md)
