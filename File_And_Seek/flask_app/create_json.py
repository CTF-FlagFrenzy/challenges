import hashlib
import json
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

with open(os.path.join(os.path.dirname(__file__), "products.json"), "r") as json_file:
    data = json.load(json_file)
    products = data["products"]

challengeflag = "#74q$j&zcB"
teamflag = os.environ.get("TEAMKEY")
combined_flag = challengeflag + teamflag

if combined_flag:
    hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
    logger.info("Flag successfully created and hashed: %s", hashed_flag)
else:
    logger.error(
        "Failed to create flag. Ensure TEAMKEY and CHALLENGEKEY are set in environment variables."
    )
    hashed_flag = "FLAG_NOT_DEFINED"


part_length = len(hashed_flag) // 9
hashed_flag_parts = [
    hashed_flag[i: i + part_length] for i in range(0, part_length * 8, part_length)
]
hashed_flag_parts.append(hashed_flag[part_length * 8:])

logger.info("Hashed flag parts created: %s", hashed_flag_parts)

for i, product in enumerate(products):
    try:
        product["id"] = hashed_flag_parts[i]
        logger.info(
            "Assigned ID %s to product %s", hashed_flag_parts[i], product["name"]
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
