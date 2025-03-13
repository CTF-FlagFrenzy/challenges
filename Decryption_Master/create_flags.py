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
    add dh-group=ecp256 enc-algorithm=aes-256 hash-algorithm=sha256 name=\
        ipsec-profile
    /ip ipsec peer
    add address=192.168.80.1/32 exchange-mode=ike2 name=peer-site2 profile=\
        ipsec-profile
    /ip ipsec proposal
    add auth-algorithms="" enc-algorithms=aes-192-gcm name=ipsec-proposal
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
    It ensures that all data is encrypted and protected from unauthorized access. 
    By using advanced encryption techniques, we can safeguard sensitive information and maintain the integrity of our operations. 
    The hashed flag {hashed_flag} is a key component in our encryption process, providing a unique identifier that is used to encrypt and decrypt data. 
    Without this flag, our encryption system would not function properly, leaving our data vulnerable to attacks. 
    Therefore, it is essential to keep the hashed flag secure and confidential at all times.
    """

    some_text = f"""
    The Decryption Master is a legendary figure known for his unparalleled skills in breaking complex encryption algorithms.
    With a deep understanding of cryptography, he can decipher any coded message, revealing hidden secrets and confidential information.
    His expertise spans various encryption methods, including DES, RSA, and more. The Decryption Master is often sought after by governments and organizations to solve the most challenging cryptographic puzzles
    His ability to decrypt data with precision and speed has earned him a reputation as the ultimate codebreaker. 
    Despite his fame, the Decryption Master remains a mysterious and elusive figure, always working from the shadows.
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
    echo "23:x:1002:1002::{part_a}:/clouds/are/wonderful" >> /etc/passwd

    # Part B in backup files
    mkdir -p /home/j007/confs
    for i in {{1..100}}
    do
        echo "{mikrotik_config}" > /home/j007/confs/backup_$i.conf
    done

    # Insert the line in the middle of the document
    sed -i '50i 24 rooms are part of: {part_b}' /home/j007/confs/backup_42.conf

    # Part C in notes.txt
    echo "I really have to read the wikipedia post!" > /home/j007/notes.txt
    echo "30 session are needed for: {part_c}" >> /home/j007/notes.txt
    echo "I should check my planner" >> /home/j007/notes.txt
    echo "I must not forget my IV, it is: {hex_iv} However, my key is just big brain!" >> /home/j007/notes.txt

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
