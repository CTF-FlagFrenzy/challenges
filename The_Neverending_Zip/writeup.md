# The Neverending Zip Challenge Writeup

## Challenge Overview
"The Neverending Zip" is a challenge that involves navigating through a deeply nested ZIP file structure (approximately 11,111 layers deep) to find a flag hidden at the core.

## Solution Approach

### Understanding the Challenge
The challenge presents us with a ZIP file that contains another ZIP file, which contains another ZIP file, and so on - creating a nesting that goes thousands of layers deep. The flag is hidden in a text file at the innermost layer.

### Method 1: Manual Solution (Not Recommended)
1. Download the initial ZIP file from the web interface
2. Extract the ZIP file manually
3. Find the next ZIP file inside
4. Repeat steps 2-3 approximately 11,111 times (clearly not practical!)

### Method 2: Automated Solution
Since manual extraction would be extremely time-consuming, we need to write a script to automate the process.

#### Step 1: Examine the Challenge
Looking at the challenge structure, we can see from the `create_zip.py` file that:
- The flag is generated using a challenge key and team key
- The ZIP nesting is approximately 11,111 layers deep
- The flag is stored in a file called `flag.txt` at the core

#### Step 2: Create an Automated Extraction Script
Create a Python script that can:
1. Accept a path to the initial ZIP file
2. Extract the contents to a temporary directory
3. Find the next ZIP file in the extracted contents
4. Repeat the process until we reach a directory with `flag.txt`
5. Read and display the flag

#### Step 3: Run the Automated Solution
1. Start with the initial `HaveFun.zip` file
2. Run our extraction script against it
3. Wait for the script to navigate through all nested layers
4. Retrieve the flag from the final `flag.txt` file

## Key Observations
- The challenge relies on the impracticality of manual extraction
- The `create_zip.py` script shows us that the flag is generated using the formula:
  ```
  combined_flag = challengekey + teamkey
  hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
  ```
- Based on the extraction process, we can see that the flags are consistent with the format "FF{...}"

## Flag
Upon reaching the core and opening `flag.txt`, we find the flag in the format `FF{...}` which is a SHA-256 hash based on the challenge and team keys.

## Lessons Learned
1. Automation is essential when dealing with repetitive tasks
2. Understanding the challenge creation process can provide insights into the solution
3. Temporary storage management is important when processing many files
4. The power of scripting allows us to solve problems that would be practically impossible manually