import hashlib
import json
import logging
import os
import random

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

with open(os.path.join(os.path.dirname(__file__), "products.json"), "r") as json_file:
    data = json.load(json_file)
    products = data["products"]

challengeflag = "t9gE6@W!Nz"
teamflag = os.environ.get("TEAMKEY")
combined_flag = challengeflag + teamflag

if combined_flag:
    hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
    logger.info("Flag successfully created and hashed: %s", hashed_flag)
else:
    logger.error(
        "Failed to create flag. Ensure TEAMKEY and CHALLENGEKEY are set in environment variables."
    )

part_length = len(hashed_flag) // 9
hashed_flag_parts = [
    hashed_flag[i: i + part_length] for i in range(0, part_length * 8, part_length)
]
hashed_flag_parts.append(hashed_flag[part_length * 8:])

logger.info("Hashed flag parts created: %s", hashed_flag_parts)

# Encode each part to hex using NONE as the delimiter
hashed_flag_parts_hex = [part.encode("utf-8").hex() for part in hashed_flag_parts]

# Shuffle the encoded parts and keep track of the original positions
original_positions = list(range(len(hashed_flag_parts_hex)))
shuffled_positions = original_positions[:]
random.shuffle(shuffled_positions)

shuffled_flag_parts_hex = [hashed_flag_parts_hex[i] for i in shuffled_positions]

logger.info("Shuffled hashed flag parts: %s", shuffled_flag_parts_hex)
logger.info("Shuffled positions: %s", shuffled_positions)

for i, product in enumerate(products):
    try:
        product["id"] = shuffled_flag_parts_hex[i]
        product["priceUsd"]["units"] = shuffled_positions[
            i
        ]  # Store the original position in the existing units field
        logger.info(
            "Assigned ID %s to product %s with units %d",
            shuffled_flag_parts_hex[i],
            product["name"],
            shuffled_positions[i],
        )
    except IndexError:
        logger.error("Not enough hashed flag parts to assign to all products")
        break

data = {"products": products}

output_path = os.path.join("flask_app/hidden", "security.txt")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as json_file:
    json.dump(data, json_file, indent=4)
logger.info("JSON file successfully created at %s", output_path)
