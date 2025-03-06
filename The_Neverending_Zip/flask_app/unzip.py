import logging
import os
import shutil
import time
import zipfile
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def extract_nested_zips(zip_path, extract_dir):
    """Recursively extract nested zip files until we find the flag."""

    # Create extract directory if it doesn't exist
    os.makedirs(extract_dir, exist_ok=True)

    # Stats tracking
    start_time = time.time()
    layer_count = 0
    last_report_time = start_time
    report_interval = 5  # Report progress every 5 seconds

    current_zip = zip_path

    try:
        while True:
            layer_count += 1
            current_extract_dir = os.path.join(extract_dir, f"layer_{layer_count}")
            os.makedirs(current_extract_dir, exist_ok=True)

            # Extract the current zip
            with zipfile.ZipFile(current_zip, "r") as zipf:
                zipf.extractall(current_extract_dir)

                # Log the contents
                contents = zipf.namelist()
                logger.debug(f"Layer {layer_count} contents: {contents}")

                # Check if we found the flag
                if "flag.txt" in contents:
                    flag_path = os.path.join(current_extract_dir, "flag.txt")
                    logger.info(f"Found flag file at layer {layer_count}!")
                    with open(flag_path, "r") as f:
                        flag_content = f.read()
                        logger.info(f"Flag content:\n{flag_content}")
                    break

                # Find the next zip file to extract
                next_zip = None
                for item in contents:
                    if item.lower().endswith(".zip"):
                        next_zip = os.path.join(current_extract_dir, item)
                        break

                if next_zip is None:
                    logger.error(
                        f"No zip file found in layer {layer_count}. Extraction complete but no flag found."
                    )
                    break

                current_zip = next_zip

            # Progress reporting
            current_time = time.time()
            if current_time - last_report_time > report_interval:
                elapsed = current_time - start_time
                extraction_rate = layer_count / elapsed if elapsed > 0 else 0
                logger.info(
                    f"Processed {layer_count} layers in {elapsed:.2f} seconds ({extraction_rate:.2f} layers/sec)"
                )
                last_report_time = current_time

            # Clean up previous layer to save disk space (optional)
            if layer_count > 1:
                prev_layer_dir = os.path.join(extract_dir, f"layer_{layer_count-1}")
                if os.path.exists(prev_layer_dir):
                    shutil.rmtree(prev_layer_dir)

    except Exception as e:
        logger.error(f"Error during extraction: {e}")
        raise

    finally:
        # Report final statistics
        end_time = time.time()
        total_time = end_time - start_time
        logger.info(f"Extraction completed after {layer_count} layers")
        logger.info(
            f"Total extraction time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)"
        )
        if layer_count > 0 and total_time > 0:
            logger.info(
                f"Average extraction rate: {layer_count/total_time:.2f} layers/second"
            )


def main():
    # Define paths
    script_dir = Path(__file__).parent.absolute()

    # Look for the zip file in the 'zip' folder instead
    zip_folder = script_dir / "zip"
    zip_path = zip_folder / "HaveFun.zip"
    extract_dir = script_dir / "unzip"

    # Check alternative locations if not found
    if not zip_path.exists():
        # Try looking in the same directory
        alternate_path = script_dir / "HaveFun.zip"
        if alternate_path.exists():
            zip_path = alternate_path
            logger.info(f"Found zip file at {zip_path}")
        else:
            logger.error(f"Zip file not found at {zip_path} or {alternate_path}")
            return

    # Create an empty extraction directory
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir)

    logger.info(f"Starting extraction of {zip_path} into {extract_dir}")
    extract_nested_zips(zip_path, extract_dir)
    logger.info("Extraction process completed")


if __name__ == "__main__":
    main()
