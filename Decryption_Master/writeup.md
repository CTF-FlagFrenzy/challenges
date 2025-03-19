# CTF Cryptography | Decryption Master Writeup: Hard Level

## Challenge Overview
This challenge involves finding parts of a ciphertext hidden in various locations, combining them in the correct order, and decrypting them using AES-128 CBC. Below are the steps to solve the challenge:

## Steps to solve
1. Retrieve the first flag
    - Start off with some basic commands, especially `history`
    - Analyse the history
    - There are wwo interesting system variables `$SystemNothing` and `$YouKnowNothing`
    - However, `$SystemNothing` includes an interesting text plus the first flag.
    - Hand in the flag using the known flag layout.

2. Locate the Ciphertext parts
    - The ciphertext is divided into four parts, all hidden in different locations.
        - Part A
            - Found in the `passwd` file.
            - Look for a line like: `u23:x:1002:1002::{part_a}:/clouds/are/wonderful`
            - Extract part a.
        - Part B
            - Found in one of the backup files in `/home/j007/confs/`
            - You may use the `diff` command.
            - Specifically, it is inserted into the middle of `backup_42.conf` using the line: `24 rooms are part of: {part_b}`
            - Extract part b.
        - Part C
            - Found in `/home/j007/notes.txt`
            - Look for a line like: `30 session are needed for: {part_c}`
            - Extract part c.
        - Part D
            - Found in `/var/log/syslog`
            - Look for a line like: `100% insanity in HTL Villach leads to: {part_d}`
            - Extract part d.

3. Combine the parts
    - Combine the parts in the correct order.
    - The used numbers in the lines of the parts indicate the order (e.g. u23 - number 23)
    - Order from the lowest to the highest number, so: `ciphertext = part_a + part_b + part_c + part_d`

4. Find the IV used for AES-128-CBC
    - The Initialization Vector (IV) is stored in `/home/j007/notes.txt`
    - Look for a line like: `I must not forget my IV, it is: {hex_iv}`
    - Extract the IV.

5. Decrypt the ciphertext using AES-128-CBC
    - Convert the combined ciphertext from hex to bytes.
    - Use the AES key (first 16 byte of the first flag) and IV to decrypt the ciphertext.
    - Unpad the decrypted data to retrieve the plaintext flag.
    - In order to achieve this, use the following Python script: 
        ```py
        import base64
        import hashlib
        import binascii
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import unpad

        # Retrieve the parts from their respective locations
        part_a = "..."  # Retrieve from /etc/passwd
        part_b = "..."  # Retrieve from /home/j007/confs/backup_21.conf
        part_c = "..."  # Retrieve from /home/j007/notes.txt
        part_d = "..."  # Retrieve from /var/log/syslog
        hex_iv = "..."  # Retrieve from /home/j007/notes.txt

        # Combine all parts to form the original ciphertext
        hex_ciphertext = part_a + part_b + part_c + part_d

        # Convert the hexadecimal ciphertext and IV to bytes
        ciphertext = bytes.fromhex(hex_ciphertext)
        iv = bytes.fromhex(hex_iv)

        # Use the AES key and IV to decrypt the ciphertext
        hashed_flag = "FF{...}"  # The hashed flag used to generate the AES key
        aes_key = hashed_flag[:16].encode('utf-8')  # 16-byte key

        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(ciphertext)
        decrypted_flag = unpad(decrypted_padded, AES.block_size).decode('utf-8')

        print(f"Decrypted Flag: {decrypted_flag}")
        ```

## Tools Used
    - Basic Linux Commands
    - Python (Hashlib, Binascii, PyCryptodome)

## Conclusion
Decryption Master was an excellent challenge that tested a wide range of cryptographic and analytical skills. It required careful exploration of system files, logical thinking to combine ciphertext parts, and a solid understanding of AES-128-CBC decryption.