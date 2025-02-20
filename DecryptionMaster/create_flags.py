#!/usr/bin/env python3
import hashlib
import logging
import os
import subprocess
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Flag creation
    challenge_flag = "j3L2k3'sz\\"
    challenge_flag_two = "4j*3$9r0Sv"
    team_flag = os.getenv("TEAMKEY")

    combined_flag = challenge_flag + team_flag
    combined_flag_two = challenge_flag_two + team_flag

    hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
    logger.info(f"Flag for history successfully created and hashed {hashed_flag}")

    hashed_flag_two = ("FF{" + hashlib.sha256(combined_flag_two.encode()).hexdigest() + "}")
    logger.info(f"Flag for AES encryption successfully created and hashed {hashed_flag_two}")

    # AES-128 Encryption (CBC mode)
    aes_key =  hashed_flag[:16].encode('utf-8') # 16-byte key
    iv = os.urandom(16) # random IV    

    # Create the cipher object and encrypt the data
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(hashed_flag_two.encode('utf-8'), AES.block_size))

    # Convert the ciphertext and IV to hexadecimal format
    hex_ciphertext = ciphertext.hex()
    hex_iv = iv.hex()
    logger.info(f"IV = {str((binascii.hexlify(iv)), "utf-8")}")
    logger.info(f"Ciphertext = {str((binascii.hexlify(ciphertext)), "utf-8")}")