#!/usr/bin/env python3
import hashlib
import os
import random

from dotenv import load_dotenv

print("Running startup script...")


load_dotenv()

team_key = os.getenv("TEAMKEY")
challenge_key = "CeaserusCipherusRichtigus"
combined_flag = challenge_key + team_key
hashed_flag = f"FF{{{hashlib.sha256(combined_flag.encode()).hexdigest()}}}"
print(f"Team Key: {team_key}")
print(f"Challenge Key: {challenge_key}")
print(f"Flag: {hashed_flag}")

print("Running startup script...")
# Add your startup logic here


def caesar_cipher(text, shift):
    """
    Encrypts a string using the Caesar cipher.

    Parameters:
    text (str): The input string to be encrypted.
    shift (int): The number of positions to shift each character.

    Returns:
    str: The encrypted string.
    """
    encrypted_text = []

    for char in text:
        if char.isalpha():
            # Determine if the character is uppercase or lowercase
            start = ord("A") if char.isupper() else ord("a")
            # Shift the character and wrap around using modulo
            encrypted_char = chr((ord(char) - start + shift) % 26 + start)
            encrypted_text.append(encrypted_char)
        else:
            # Non-alphabetic characters are added as is
            encrypted_text.append(char)

    return "".join(encrypted_text)


random_shift = random.randint(1, 25)

# Example usage
encrypted_text = caesar_cipher(hashed_flag, shift=random_shift)


html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flag</title>
</head>
<body>
    <h1>Some weird text has been found: {encrypted_text}</h1>
</body>
</html>
"""

# Write HTML content to a file
output_path = "/usr/local/apache2/htdocs/index.html"
with open(output_path, "w") as file:
    file.write(html_content)

print(f"HTML file written to {output_path}")
