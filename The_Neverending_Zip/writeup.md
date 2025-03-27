# CTF Automation | The Neverending Zip Challenge Writeup: Hard Level

## Challenge Overview
"The Neverending Zip" is a challenge that tests participants' automation skills by requiring them to navigate through a deeply nested ZIP file structure (approximately 11,111 layers deep) to find a flag hidden at the core.

## Steps to Solve

### 1. Download the Initial ZIP File
- Download the `HaveFun.zip` file from the web interface
- This is just the beginning of the challenge - there are many layers beneath!

### 2. Understand the Challenge Structure
- Examining the challenge reveals that:
  - The ZIP contains approximately 11,111 nested layers
  - Each ZIP file contains another ZIP file inside it
  - The flag is stored in a `flag.txt` file at the innermost layer
  - Manual extraction would be extremely impractical

![Picture could not be loaded](./media/zip_depth_illustration.png)

### 3. Analyze the Challenge Creation Process
From the `create_zip.py` file, we can understand how the challenge was constructed:
- The flag is generated using a challenge key and team key
- The formula used is:
  ```python
  combined_flag = challengekey + teamkey
  hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
  ```
- The ZIP nesting is achieved through a loop that creates approximately 11,111 layers

### 4. Create an Automated Extraction Script
Since manual extraction would take days, we need to create a Python script that can:

```python
import os
import zipfile
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_nested_zips(zip_path, extract_dir):
    """Recursively extract nested zip files until we find the flag."""
    os.makedirs(extract_dir, exist_ok=True)
    
    # Stats tracking
    start_time = time.time()
    layer_count = 0
    
    current_zip = zip_path
    
    try:
        while True:
            layer_count += 1
            current_extract_dir = os.path.join(extract_dir, f"layer_{layer_count}")
            os.makedirs(current_extract_dir, exist_ok=True)
            
            # Report progress every 100 layers
            if layer_count % 100 == 0:
                elapsed = time.time() - start_time
                layers_per_second = layer_count / elapsed if elapsed > 0 else 0
                logger.info(f"Processed {layer_count} layers. Speed: {layers_per_second:.2f} layers/sec")
            
            # Extract the current zip
            with zipfile.ZipFile(current_zip, "r") as zipf:
                zipf.extractall(current_extract_dir)
                
                # Check if we found the flag
                if "flag.txt" in zipf.namelist():
                    flag_path = os.path.join(current_extract_dir, "flag.txt")
                    logger.info(f"Found flag file at layer {layer_count}!")
                    with open(flag_path, "r") as f:
                        flag_content = f.read()
                        logger.info(f"Flag content:\n{flag_content}")
                    return flag_content
                
                # Find the next zip file
                next_zip = None
                for item in zipf.namelist():
                    if item.lower().endswith(".zip"):
                        next_zip = os.path.join(current_extract_dir, item)
                        break
                
                if next_zip is None:
                    logger.error("No zip file found in layer. Extraction complete but no flag found.")
                    break
                
                current_zip = next_zip
                
                # Clean up previous layer to save space (optional)
                # if layer_count > 1:
                #     prev_layer_dir = os.path.join(extract_dir, f"layer_{layer_count-1}")
                #     shutil.rmtree(prev_layer_dir, ignore_errors=True)
                
    except Exception as e:
        logger.error(f"Error during extraction: {e}")
        return None

# Usage
if __name__ == "__main__":
    zip_path = "HaveFun.zip"  # Path to the initial zip file
    extract_dir = "extracted"  # Directory to extract files to
    
    logger.info(f"Starting extraction of {zip_path}")
    extract_nested_zips(zip_path, extract_dir)
```

### 5. Run the Script and Wait
- Execute the extraction script against the initial ZIP file
- The script will navigate through all the nested ZIP layers
- This could take some time (10-30 minutes depending on system performance)
- Monitor the progress through the script's logging

### 6. Retrieve the Flag
Once the script reaches the core, it will find and open `flag.txt` which contains the flag in the format `FF{...}`.

## Tools Used
- Python 3.x
- Python's zipfile module
- Text editor for script creation

## Flag
The final flag is in the format `FF{...}` which is a SHA-256 hash based on the challenge and team keys.

## Lessons Learned
1. Automation is essential when dealing with repetitive tasks at scale
2. Understanding the challenge creation process can provide insights for efficient solution development
3. Memory and storage management are important when processing many nested files
4. There's a significant difference between theoretically possible manual solutions and practically feasible automated solutions