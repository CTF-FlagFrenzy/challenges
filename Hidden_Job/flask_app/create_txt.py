import hashlib
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_robots_txt():
    challengeflag_2 = os.environ.get("CHALLENGEKEY_2")
    teamflag = os.environ.get("TEAMKEY")
    download_link = f"/download/ProjectDelta.zip"
    combined_flag_2 = str(challengeflag_2) + str(teamflag)

    if combined_flag_2:
        hashed_flag_2 = (
            "FF{" + hashlib.sha256(combined_flag_2.encode()).hexdigest() + "}"
        )
        logger.info(f"Flag successfully created Flag: {hashed_flag_2} for robots.txt")

        base_hidden_folder = "hidden"
        os.makedirs(base_hidden_folder, exist_ok=True)

        robots_txt_path = os.path.join(base_hidden_folder, "robots.txt")
        with open(robots_txt_path, "w") as file:
            file.write(
                f"\nSophie: Hey Fabio, have you played Project Delta yet? The one everyone’s talking about? You can download it here : {download_link}\n"
            )
            file.write(
                "Fabio: Ohh, yeah! The one with the open world and those alien ruins, right?\n"
            )
            file.write(
                "Sophie: Yup, that’s the one! I started yesterday, and I totally messed up on the first mission. I thought it was still the tutorial and wasted all my resources.\n"
            )
            file.write(
                "Fabio: Hahaha, classic Sophie. But no joke, I didn’t realize how important the energy cores were until I accidentally sold two of them.\n"
            )
            file.write(
                "Sophie: Oof, that hurts. Have you fought that boss in the Twilight Gorge yet?\n"
            )
            file.write(
                "Fabio: Oh my god, yes! The one with the three phases? That guy absolutely destroyed me.\n"
            )
            file.write(
                "Sophie: Right?! I was so proud when I cleared the first phase, and then BAM – he pulls out those laser drones.\n"
            )
            file.write(
                "Fabio: Ugh, those things are so unfair. I burned through like five revival kits just to survive.\n"
            )
            file.write(
                "Sophie: Same. If I hadn’t gotten the jetpack upgrade, I wouldn’t have stood a chance. It saved my life.\n"
            )
            file.write("Fabio: Jetpack upgrade?! Where did you get that?!\n")
            file.write(f"Sophie: Haha, You need to enter this {hashed_flag_2}.\n")
            file.write("Fabio: Ugh, you’re the best.\n")
            file.write(
                "Sophie: Trust me, it’s worth it. But just wait – the next boss is ten times harder.\n"
            )
            file.write(
                "Fabio: Stop trying to scare me! I need a break after all this stress.\n"
            )

        logger.info("robots.txt file created at %s", robots_txt_path)
    else:
        logger.error(
            "Failed to create flag. Ensure TEAMKEY and CHALLENGEKEY_2 are set in environment variables."
        )


if __name__ == "__main__":
    create_robots_txt()
