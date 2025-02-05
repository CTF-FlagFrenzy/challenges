#!/usr/bin/env python3
import hashlib
import logging
import os
import subprocess
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    challenge_flag = "j3L2k3'sz\\"
    challenge_flag_two = "4j*3$9r0Sv"
    team_flag = os.getenv("TEAMKEY")

    combined_flag = challenge_flag + team_flag
    combined_flag_two = challenge_flag_two + team_flag

    hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
    logger.info(f"Flag for history successfully created and hashed {hashed_flag}")

    hashed_flag_two = ("FF{" + hashlib.sha256(combined_flag_two.encode()).hexdigest() + "}")
    logger.info(f"Flag for AES encryption successfully created and hashed {hashed_flag_two}")

    # cipher = AES.new(hashed_flag.encode('utf-8'), AES.MODE_CBC)
    # ct_bytes = cipher.encrypt(pad(hashed_flag_two.encode('utf-8'), AES.block_size))
    