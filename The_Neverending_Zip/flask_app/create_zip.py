import argparse
import hashlib
import json
import logging
import os
import shutil
import tempfile
import time
import zipfile

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_recursive_zip(status_file=None):
    start_time = time.time()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)  # Go up one level from flask_app/
    hidden_dir = os.path.join(parent_dir, "zip")

    logger.info(f"Creating zip directory at: {hidden_dir}")
    os.makedirs(hidden_dir, exist_ok=True)

    # Generate flag based on challenge and team key
    challengekey = "F34rLh3Z1p"
    teamkey = os.environ.get("TEAMKEY")
    if not teamkey:
        logger.warning("TEAMKEY environment variable not set, using default")
        teamkey = "default_key"

    combined_flag = challengekey + teamkey
    hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"

    logger.info(f"Creating deeply nested zip with flag: {hashed_flag}")

    # Create the deeply nested zip structure
    temp_dir = tempfile.mkdtemp()
    try:
        # Create the innermost file containing the flag
        flag_file_path = os.path.join(temp_dir, "flag.txt")
        with open(flag_file_path, "w") as flag_file:
            flag_file.write(f"Congratulations! You've reached the core of the zip!\n")
            flag_file.write(f"Your flag is: {hashed_flag}\n")
            flag_file.write(f"\n")
            flag_file.write(f"This zip was nested {11111} layers deep.\n")
            flag_file.write(f"Your persistence is admirable!\n")

        # Create a README to explain the challenge
        readme_path = os.path.join(temp_dir, "README.txt")
        with open(readme_path, "w") as readme:
            readme.write("THE NEVERENDING ZIP CHALLENGE\n\n")
            readme.write("This zip file contains another zip file...\n")
            readme.write("which contains another zip file...\n")
            readme.write("which contains another zip file...\n")
            readme.write("and so on for many layers.\n\n")
            readme.write("Can you reach the center to find the flag?\n")
            readme.write("Good luck! You're going to need it.\n")

        # Use consistent ZIP filename for all layers
        zip_filename = "HaveFun.zip"

        # Start with the flag file in a zip
        inner_zip_path = os.path.join(temp_dir, "inner.zip")
        with zipfile.ZipFile(
            inner_zip_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as zipf:
            zipf.write(flag_file_path, arcname="flag.txt")

        current_zip = inner_zip_path
        max_layers = 11111
        batch_size = 1000

        for layer in range(1, max_layers + 1):
            prev_zip = current_zip
            current_zip = os.path.join(temp_dir, f"temp_layer_{layer}.zip")

            # Simple zip creation - always use the same name for the inner zip
            with zipfile.ZipFile(
                current_zip, "w", compression=zipfile.ZIP_DEFLATED
            ) as zipf:
                zipf.write(prev_zip, arcname=zip_filename)

            # Delete the previous zip to save space
            os.remove(prev_zip)

            # Add some performance optimization - flush log handler periodically
            if layer % batch_size == 0:
                for handler in logger.handlers:
                    handler.flush()

                # Display performance metrics every batch_size layers
                current_time = time.time()
                elapsed = current_time - start_time
                layers_per_second = layer / elapsed if elapsed > 0 else 0
                estimated_total = (
                    max_layers / layers_per_second if layers_per_second > 0 else 0
                )
                remaining = estimated_total - elapsed

                # Aktualisiere Statusdatei
                if status_file and os.path.exists(os.path.dirname(status_file)):
                    try:
                        with open(status_file, "w") as f:
                            json.dump(
                                {
                                    "start_time": start_time,
                                    "current_time": current_time,
                                    "progress": layer / max_layers,
                                    "estimated_total_time": estimated_total,
                                    "remaining_time": remaining,
                                    "layers_per_second": layers_per_second,
                                },
                                f,
                            )
                    except Exception as e:
                        logger.error(f"Fehler beim Aktualisieren der Statusdatei: {e}")

                logger.info(
                    f"Performance: {layers_per_second:.1f} layers/sec | "
                    + f"Est. remaining: {remaining/60:.1f} minutes | "
                    + f"Progress: {layer/max_layers*100:.2f}%"
                )

        # Create the final zip with the deepest nested zip and the README
        final_layer_path = os.path.join("flask_app/zip", "HaveFun.zip")
        with zipfile.ZipFile(
            final_layer_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as zipf:
            zipf.write(current_zip, arcname=zip_filename)
            zipf.write(readme_path, arcname="README.txt")

        end_time = time.time()
        total_time = end_time - start_time
        logger.info(f"Deeply nested zip created at {final_layer_path}")
        logger.info(
            f"Total creation time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)"
        )

        # Letzte Aktualisierung der Statusdatei
        if status_file and os.path.exists(os.path.dirname(status_file)):
            try:
                with open(status_file, "w") as f:
                    json.dump(
                        {
                            "start_time": start_time,
                            "end_time": end_time,
                            "progress": 1.0,
                            "estimated_total_time": total_time,
                            "remaining_time": 0,
                            "complete": True,
                        },
                        f,
                    )
            except Exception as e:
                logger.error(f"Fehler beim Aktualisieren der Statusdatei: {e}")

        return final_layer_path

    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Erstellt eine rekursiv verschachtelte ZIP-Datei"
    )
    parser.add_argument(
        "--status-file", type=str, help="Pfad zur Statusdatei", default=None
    )
    args = parser.parse_args()

    create_recursive_zip(args.status_file)
