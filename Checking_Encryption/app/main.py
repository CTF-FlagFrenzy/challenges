import hashlib
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse

if os.environ.get("TEAMKEY") is None:
    load_dotenv()

team_key = os.getenv("TEAMKEY")
challenge_key = "VeryLongUnpredictableStringWithNoMeaningWhatsoeverItsTheChallengeKey"
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
