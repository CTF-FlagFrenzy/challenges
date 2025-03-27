# Checking Encryption

## Challenge Description

This challenge provides the user with an encoded string that looks almost like a flag, such as `FF{Ľc1cĬca3Į1afĩ09bı4aeĲ52cü911þ0e0ł`. The goal is to reverse the custom encoding algorithm to retrieve the original flag.

The encoding process uses a custom algorithm called `checksumming`. This algorithm modifies the string by summing the Unicode values of every `n` characters (where `n` is the checksum interval) and replacing the last character in the group with the sum. The resulting string is then presented as the encoded flag.

---

## Encoding Algorithm

The encoding algorithm works as follows:

1. Convert each character in the input string to its Unicode integer value using the `ord()` function.
2. For every `n` characters (where `n` is the checksum interval), calculate the sum of their Unicode values.
3. Replace the last character in the group with the character corresponding to the sum of the Unicode values using the `chr()` function.
4. Repeat this process for the entire string.

For example, with a checksum interval of 4 and the input `FF{6`:
```
F - 70
F - 70
{ - 123
6 - 54

70 + 70 + 123 + 54 = 317

Result:
F - 70
F - 70
{ - 123
Ľ - 317
```

---

## Decoding Algorithm

To decode the string, the process is reversed:

1. For every `n` characters (where `n` is the checksum interval), calculate the sum of the Unicode values of the first `n-1` characters.
2. Subtract this sum from the Unicode value of the `n`th character to retrieve the original Unicode value of the last character in the group.
3. Replace the `n`th character with the original character.
4. Repeat this process for the entire string.

Here is the Python implementation of the decoding algorithm:
```python
def undoChecksumming(message, checksum_interval=4):
    if checksum_interval < 1:
        print("Checksum interval must be at least 2")
        return
    result_message = ""
    charIdx = 1
    for char in message:
        chached_char = char
        if charIdx % checksum_interval == 0:
            # Get Unicode sum of the current and the characters before according to the checksum_interval
            sum = getStringUnicodeSum(char) - getStringUnicodeSum(message[charIdx-checksum_interval:charIdx-1])
            # Convert Unicode to char
            chached_char = chr(sum)
        charIdx += 1
        result_message += chached_char
    return result_message
```

---

## Steps to Solve

1. Retrieve the encoded string from the provided file or FastAPI endpoint.
2. Analyze the encoding algorithm to understand how the string was transformed.
3. Implement the decoding algorithm (`undoChecksumming`) in Python or another programming language.
4. Use the decoding algorithm to reverse the transformation and retrieve the original flag.

---

## Example Solution

Given the encoded string `FF{Ľc1cĬca3Į1afĩ09bı4aeĲ52cü911þ0e0ł` and a checksum interval of 4:

1. Use the `undoChecksumming` function to decode the string.
2. The output will be the original flag, e.g., `FF{example_flag}`.

---

## Tools and Environment

- **Programming Language**: Python
- **Dependencies**: FastAPI, dotenv
- **Environment**: Dockerized Python 3.9 application

To set up the environment, follow the installation instructions in the `Checking_Encryption.md` file.

---

## Conclusion

This challenge tests the participant's ability to analyze and reverse-engineer custom encoding algorithms. By understanding the encoding process and implementing the decoding algorithm, participants can successfully retrieve the original flag.