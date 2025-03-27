# Mental Overflow Challenge Writeup

## Challenge Overview
Mental Overflow is a web-based CTF challenge that provides a file called `challenge.bin`. The goal is to decode this file and extract the flag.

## Solution

### Step 1: Download the File
When visiting the challenge website, you'll be redirected to download a file called `challenge.bin`.

### Step 2: Decode the Base64
The `challenge.bin` file contains Base64-encoded data. First, decode it:

```bash
cat challenge.bin | base64 -d > decoded.bf
```

### Step 3: Understand the Content
The decoded content is a Brainfuck program. Brainfuck is an esoteric programming language with eight simple commands.

### Step 4: Execute the Brainfuck Code
Use any Brainfuck interpreter to run the decoded program:

```bash
# Using an online interpreter:
# Copy the content of decoded.bf to an online Brainfuck interpreter
# Such as: https://copy.sh/brainfuck/

# Or using a command-line interpreter:
bf decoded.bf
```

### Step 5: Analyze the Output
The Brainfuck program outputs text that looks similar to a flag but with some characters replaced. The output will be in a format like:
```
FF"HASH_VALUE"
```
where the curly braces of a typical flag format have been replaced with random characters.

### Step 6: Format the Flag Correctly
Replace the random characters with curly braces to get the proper flag format:
```
FF{HASH_VALUE}
```

### Step 7: Submit the Flag
Submit the correctly formatted flag to complete the challenge.

## Key Insights
1. The challenge involves multiple layers of encoding (Base64 + Brainfuck)
2. The flag format is intentionally obfuscated by replacing the curly braces with random characters
3. Understanding how to decode Base64 and execute Brainfuck code is essential to solving the challenge

## Tools Used
- Base64 decoder
- Brainfuck interpreter (online or command-line)