#!/usr/bin/env python3
import hashlib
import logging
import os
import subprocess
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# AES SubBytes table
SUBBYTES_TABLE = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
]

def apply_subbytes(key_bytes):
    # Apply AES SubBytes transformation to the key.
    return bytes(SUBBYTES_TABLE[b] for b in key_bytes)

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

    hashed_flag = hashlib.sha256(combined_flag.encode()).hexdigest()
    hashed_flag_formatted = "FF{" + hashed_flag + "}"
    logger.info(f"First flag created (history): {hashed_flag_formatted}")

    hashed_flag_two = ("FF{" + hashlib.sha256(combined_flag_two.encode()).hexdigest() + "}")
    logger.info(f"Second flag created (AES): {hashed_flag_two}")

    # AES-128 Encryption (CBC mode)
    # Extract the first 16 bytes of the hashed flag and apply SubBytes
    raw_key = bytes.fromhex(hashed_flag_formatted[:16].encode('utf-8').hex()) # 16-byte key)
    aes_key = apply_subbytes(raw_key)

    logger.info(f"AES key (RAW): {raw_key.hex()}")
    logger.info(f"AES key (SB): {aes_key.hex()}")

    iv = os.urandom(16) # random IV 
    iv_new = apply_subbytes(iv)

    # Create the cipher object and encrypt the data
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(hashed_flag_two.encode('utf-8'), AES.block_size))

    # Convert the ciphertext and IV to hexadecimal format
    hex_ciphertext = ciphertext.hex()
    logger.info(f"IV (RAW) = {str((binascii.hexlify(iv)), "utf-8")}")
    logger.info(f"IV (SB) = {str((binascii.hexlify(iv_new)), "utf-8")}")
    logger.info(f"Ciphertext = {str((binascii.hexlify(ciphertext)), "utf-8")}")

    # Divide the ciphertext into 4 parts
    part_size = len(hex_ciphertext) // 4
    part_a = hex_ciphertext[:part_size]
    part_b = hex_ciphertext[part_size:2*part_size]
    part_c = hex_ciphertext[2*part_size:3*part_size]
    part_d = hex_ciphertext[3*part_size:]

    # Mikrotik RouterOS configuration
    mikrotik_config = f"""
    # 2025-01-06 18:13:38 by RouterOS 7.16.1
    # software id = 
    #
    /interface bridge
    add name=bridge1
    add name=loopback1
    /interface gre
    add local-address=10.18.202.1 name=gre-1 remote-address=10.18.101.1
    /ip ipsec profile
    add dh-group=ecp256 enc-algorithm=hello hash-algorithm=sha256 name=\
        ipsec-profile
    /ip ipsec peer
    add address=192.168.80.1/32 exchange-mode=ike2 name=peer-site2 profile=\
        ipsec-profile
    /ip ipsec proposal
    add auth-algorithms="" enc-algorithms=hello-gcm name=ipsec-proposal
    /port
    set 0 name=serial0
    set 1 name=serial1
    /routing ospf instance
    add disabled=no name=ospf-1 router-id=172.18.18.1
    /routing ospf area
    add disabled=no instance=ospf-1 name=ospf-area-0
    /interface bridge port
    add bridge=bridge1 interface=ether2
    add bridge=bridge1 interface=ether3
    add bridge=bridge1 interface=ether4
    /ip address
    add address=10.18.202.1/24 interface=bridge1 network=10.18.202.0
    add address=192.168.90.1/24 interface=ether1 network=192.168.90.0
    add address=172.18.18.1 interface=loopback1 network=172.18.18.1
    add address=10.255.255.1/30 interface=gre-1 network=10.255.255.0
    /ip dhcp-client
    add interface=ether1
    /ip firewall filter
    add action=accept chain=input dst-port=1194 protocol=tcp
    /ip ipsec identity
    add peer=peer-site2 secret="111"
    /ip ipsec policy
    set 0 disabled=yes
    add dst-address=10.18.101.0/24 peer=peer-site2 proposal=\
        ipsec-proposal src-address=10.18.202.0/24 tunnel=yes
    /ip route
    add disabled=no distance=1 dst-address=0.0.0.0/0 gateway=gre-1 \
        routing-table=main scope=30 suppress-hw-offload=no target-scope=10
    /routing ospf interface-template
    add area=ospf-area-0 disabled=no interfaces=ether1 type=ptp
    /system identity
    set name=MT18_01
    /system note
    set show-at-login=no
    /tool romon
    set enabled=yes
    """

    # Create a bash script to configure the system
    variable_text = f"""
    This flag is crucial for the security of our system. 
    It ensures integrity of data of any kind and is vital in general. 
    By using hashing techniques, we can safeguard sensitive information and maintain the integrity of our operations. 
    The hashed flag {hashed_flag}, without its usual layout, is a key component for the security in our company.
    """

    some_text = f"""
    The Decryption Master is a legendary figure known for his unparalleled skills in breaking complex encryption algorithms.
    With a deep understanding of cryptography, he can decipher any coded message, revealing hidden secrets and confidential information.
    His expertise spans various encryption methods, including DES, RSA, and more. The Decryption Master is often sought after by governments and organizations to solve the most challenging cryptographic puzzles
    """

    bash_script = f"""
    #!/bin/bash
    # Some entries in resolv.conf
    echo "#nameserver 128.128.128.128" >> /etc/resolv.conf
    echo "#gotta know how to use my CBC" >> /etc/resolv.conf
    echo "nameserver 8.8.8.8" >> /etc/resolv.conf
    echo "nameserver 1.1.1.1" >> /etc/resolv.conf
    echo "nameserver 8.8.4.4" >> /etc/resolv.conf

    mkdir /home/j007/Desktop
    mkdir /home/j007/Documents
    mkdir /home/j007/Downloads
    mkdir /home/j007/Music
    mkdir /home/j007/Pictures
    mkdir /home/j007/Videos

    touch /home/j007/Desktop/flag.txt
    echo "{some_text}" > /home/j007/Desktop/flag.txt
    touch /home/j007/Documents/document.txt
    echo "This is a confidential document" > /home/j007/Documents/document.txt
    touch /home/j007/Downloads/important.zip
    echo "This is an encrypted file" > /home/j007/Downloads/important.zip
    touch /home/j007/Music/song.mp3
    echo "This is a music file" > /home/j007/Music/song.mp3
    touch /home/j007/Pictures/photo.jpg
    echo "This is a picture file" > /home/j007/Pictures/photo.jpg
    touch /home/j007/Videos/video.mp4
    echo "This is a video file" > /home/j007/Videos/video
    echo "{some_text}" > /home/j007/Videos/video.txt

    # Add a system variable "SystemNothing"
    export SystemNothing="{variable_text}"
    echo "export SystemNothing='{variable_text}'" >> /home/j007/.bashrc

    # Part A in /etc/passwd
    echo "u23:x:1002:1002::/home/{part_a}:/clouds/are/wonderful" >> /etc/passwd

    # Part B in backup files
    mkdir /home/j007/confs
    for i in {{1..100}}
    do
        echo "{mikrotik_config}" > /home/j007/confs/backup_$i.conf

        if [ $i -eq 42 ]; then
            echo "    24 rooms are part of: {part_b}" >> /home/j007/confs/backup_$i.conf
        else
            echo "    24 rooms are part of: caa48714f1a477bb887b2a7cb7bc6d8e377d43c0" >> /home/j007/confs/backup_$i.conf
        fi

    done

    # Part C in rockyou.txt
    echo "I really have to read the wikipedia post!" >> /usr/share/wordlists/rockyou.txt
    echo "30 sessions are needed for: {part_c}" >> /usr/share/wordlists/rockyou.txt
    echo "I must not forget my IV, it is: {iv_new.hex()} However, everything is big brain!" >> /usr/share/wordlists/rockyou.txt

    # Part D in /var/log
    echo "100% insanity in HTL Villach leads to: {part_d}" >> /var/log/syslog

    # Clear the history
    history -c

    # Create a fake history with 32 lines
    history_commands=(
        "ls -la"
        "cd /var/log"
        "cat syslog"
        "sudo apt update"
        "sudo apt upgrade -y"
        "curl https://en.wikipedia.org/wiki/Advanced_Encryption_Standard"
        "git status"
        "git pull"
        "nano /etc/hosts"
        "ping -c 4 google.com"
        "df -h"
        "free -m"
        "top"
        "echo '\$SystemNothing'"
        "htop"
        "ps aux"
        "netstat -tuln"
        "ifconfig"
        "ip a"
        "echo '\$YouDontKnowMe'"
        "mkdir new_folder"
        "rm -rf old_folder"
        "cp file1 file2"
        "mv file1 /tmp/"
        "chmod +x script.sh"
        "chown user:user file"
        "echo 'Hello World'"
        "curl http://example.com"
        "wget http://example.com/file"
        "tar -xzvf archive.tar.gz"
        "zip -r archive.zip folder"
        "unzip archive.zip"
    )

    for cmd in "${{history_commands[@]}}"
    do
        echo "$cmd" >> /home/j007/.bash_history
    done
    """

    # Write the bash script to a file
    with open("configure_system.sh", "w") as file:
        file.write(bash_script)

    # Make the bash script executable
    subprocess.run(["chmod", "+x", "configure_system.sh"])

    # Execute the bash script
    subprocess.run(["/bin/bash", "./configure_system.sh"])

    # Delete the bash script after execution
    os.remove("configure_system.sh")

    logger.info(f"Script executed and deleted.")
