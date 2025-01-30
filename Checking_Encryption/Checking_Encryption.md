# Checking Encryption

A crypto challenge with the goal to decipher a string
**Level**: Hard



## Challenge Overview:

The user gets a string and has to figure out how this string was encoded and then reverse the encoding. A custom encoding is used that can not be read. 
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
For encoding the string a function called `checksumming(message, checksum_interval=3)` is used. It converts the whole message into unicode integers, it the sums up every 3 (if the `checksum_interval` is default) integers and replaces the last of those three with the result. The string is then converted back into unicode letters. This results in a string that looks almost like the flag but not quite: `FF{ľad0Ħe5aĭ709Ð844Ñ84dĴ6a9Ĳb88ć263Ę`. 


```python
import hashlib
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse

if os.environ.get("TEAMKEY") is None:
    load_dotenv()

team_key = os.getenv("TEAMKEY")
challenge_key = os.getenv("CHALLENGE")
combined_flag = challenge_key + team_key
hashed_flag = f"FF{{{hashlib.md5(combined_flag.encode()).hexdigest()}}}"
print(f"Team Key: {team_key}")
print(f"Challenge Key: {challenge_key}")
print(f"Flag: {hashed_flag}")


def checksumming(message, checksum_interval=3):
    if checksum_interval < 1:
        print("Checksum interval must be at least 2")
        return

    result_message = ""
    charIdx = 1
    for char in message:
        chached_char = char
        # every third character gets checksummed. This means that its unicode
        # value is combined with the unicode value of the 2 characters before it
        # and then the result gets printed instead of the original character
        if charIdx % checksum_interval == 0:
            # get unicode sum of the current and the 2 before
            sum = getStringUnicodeSum(message[charIdx - checksum_interval: charIdx])
            # convert unicode to char
            chached_char = chr(sum)
            print(sum)
        charIdx += 1
        result_message += chached_char
    return result_message


def getStringUnicodeSum(characters=""):
    if characters is None or characters == "":
        return 0
    sum = 0
    for character in characters:
        sum += ord(character)
    return sum


def convertToUnicode(message):
    unicode_message = ""
    for char in message:
        unicode_message += str(ord(char)) + " "
    return unicode_message


def undoChecksumming(message, checksum_interval=3):
    if checksum_interval < 1:
        print("Checksum interval must be at least 2")
        return
    result_message = ""
    charIdx = 1
    for char in message:
        chached_char = char
        if charIdx % checksum_interval == 0:
            # get unicode sum of the current and the 2 before
            sum = getStringUnicodeSum(char) - getStringUnicodeSum(
                message[charIdx - checksum_interval: charIdx - 1]
            )
            # convert unicode to char
            chached_char = chr(sum)
        charIdx += 1
        result_message += chached_char
    return result_message


# this describes the difficultiy of the checksumming, higher numbers do
# less modifications, therefore making it easier to figure out the
# algorithm
result = checksumming(hashed_flag, 4)
print(result)
result_unicode = convertToUnicode(result)
result_reverted = undoChecksumming(result, 4)
# print(result_unicode)
# print(result_reverted)

with open("encoded.txt", "w") as file:
    file.write(result)


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

Then you navigate to the root of the `Checking_Encryption` challenge and type the following command in the cli.

```
docker-compose up
```

You can see all running container with `docker ps`.

**HAVE FUN**

> [!NOTE]
> If you have any problems solving this challenge you can find a full guide [here](https://github.com/CTF-FlagFrenzy/challenges/blob/main/Checking_Encryption/writeup.md)
