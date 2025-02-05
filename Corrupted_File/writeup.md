# Corrupted File Writeup

This challenge provides the user with a file that has a corrupted signature. The task is to identify the corruption, correct the file signature, and extract the contents to find the hidden flag.

## Steps to Solve the Challenge:

1. **Identify the Corruption:**
   - The provided file has its first two bytes altered from `0x1f 0x8b` (the signature for a gzip file) to `0x00 0x00`.
   - Use a hex editor or a similar tool to inspect the first few bytes of the file.

2. **Correct the File Signature:**
   - Change the first two bytes back to `0x1f 0x8b` to restore the gzip file signature.
   - This can be done using a hex editor or a simple Python script.

3. **Extract the Contents:**
   - Once the file signature is corrected, use a tool like `tar` to extract the contents of the tar.gz archive.
   - The extracted file will contain the flag.

### Example Python Script to Correct the File Signature:

```python
def correct_file_signature(file_path):
    with open(file_path, 'r+b') as f:
        f.seek(0)  # Move to the beginning of the file
        f.write(b'\x1f\x8b')  # Write the correct gzip signature

# Usage
correct_file_signature('document')
```

### Extracting the Contents:

After correcting the file signature, you can extract the contents using the following command:

```sh
tar -xzf document
```

This will extract the `flag.txt` file containing the flag.

**HAVE FUN**

> [!NOTE]
> If you have any problems solving this challenge, you can find a full guide [here](https://github.com/CTF-FlagFrenzy/challenges/blob/main/Corrupted_File/writeup.md)