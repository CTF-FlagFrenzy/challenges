import os
import hashlib
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

def create_robots_txt(team_id):
    challengeflag_2 = os.environ.get("CHALLENGEKEY_2")
    teamflag = os.environ.get("TEAMKEY")
    combined_flag_2 = challengeflag_2 + teamflag

    if combined_flag_2:
        hashed_flag_2 = "FF{" + hashlib.sha256(combined_flag_2.encode()).hexdigest() + "}"
        logger.info("Flag successfully created and hashed for team %s: %s", team_id, hashed_flag_2)
        
        base_hidden_folder = "hidden"
        os.makedirs(base_hidden_folder, exist_ok=True)
        
        robots_txt_path = os.path.join(base_hidden_folder, "robots.txt")
        with open(robots_txt_path, "w") as file:
            file.write(f"User-agent: *\nDisallow: /\n\n# Flag: {hashed_flag_2}\n")
        
        logger.info("robots.txt file created at %s", robots_txt_path)
    else:
        logger.error(
            "Failed to create flag. Ensure TEAMKEY and CHALLENGEKEY_2 are set in environment variables."
        )

if __name__ == "__main__":
    team_id = "example_team_id"
    create_robots_txt(team_id)