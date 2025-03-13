import hashlib
import logging
import os

import piexif

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

challengeflag = "T1#mXeG24B"
teamflag = os.environ.get("TEAMKEY")
combined_flag = challengeflag + teamflag if challengeflag and teamflag else None

if combined_flag:
    hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
    logger.info("Flag successfully created and hashed: %s", hashed_flag)
else:
    logger.error(
        "Failed to create flag. Ensure TEAMKEY and CHALLENGEKEY are set in environment variables."
    )
    hashed_flag = "FLAG_NOT_DEFINED"

# Define the paths
base_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_dir, "hacker.jpg")
static_dir = os.path.join(base_dir, "static")
modified_image_path = os.path.join(static_dir, "image_with_flag.jpg")

# Load the existing image
if not os.path.exists(image_path):
    logger.error(f"Image not found at path: {image_path}")
    raise FileNotFoundError(f"Image not found at path: {image_path}")

# Load the image and its EXIF data
try:
    exif_dict = piexif.load(image_path)
except ValueError as e:
    if str(e) == "doesnot have exif":
        logger.info("Image does not have EXIF data, creating new EXIF data.")
        exif_dict = {
            "0th": {},
            "Exif": {},
            "GPS": {},
            "Interop": {},
            "1st": {},
            "thumbnail": None,
        }
    else:
        raise

# Add the flag to the image metadata
exif_dict["0th"][piexif.ImageIFD.ImageDescription] = hashed_flag
exif_bytes = piexif.dump(exif_dict)

# Ensure the static directory exists
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# Save the modified image with metadata
piexif.insert(exif_bytes, image_path, modified_image_path)

logger.info(
    "Flag successfully added to the image metadata and saved as: %s",
    modified_image_path,
)
