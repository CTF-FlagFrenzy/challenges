import hashlib
import logging
import os
import shutil
import subprocess
from scapy.all import rdpcap, wrpcap, Raw, IP, TCP

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

def create_flag():
    """Create a flag using environment variables."""
    challengekey = os.environ.get("CHALLENGEKEY", "CaptureTheBytes")
    teamkey = os.environ.get("TEAMKEY")
    
    if not teamkey:
        logger.warning("TEAMKEY environment variable not set, using default")
        teamkey = "default_key"
    
    combined_flag = challengekey + teamkey
    hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
    
    logger.info(f"Flag created: {hashed_flag}")
    return hashed_flag

def insert_flag_into_pcap(input_pcap, output_pcap, flag):
    """Insert the flag into a specific packet in the PCAP file."""
    try:
        # Read the original PCAP file
        packets = rdpcap(input_pcap)
        logger.info(f"Loaded {len(packets)} packets from {input_pcap}")
        
        if len(packets) < 1000:
            logger.warning("PCAP file has fewer packets than expected")
        
        # Choose specific packets to modify
        # We'll modify an HTTP packet (TCP port 80) to contain our flag
        flag_inserted = False
        
        # Try to find a suitable HTTP packet
        for i, packet in enumerate(packets):
            if IP in packet and TCP in packet and packet[TCP].dport == 80 and Raw in packet:
                # Get the original payload
                original_payload = bytes(packet[Raw])
                
                # Create a new payload with our flag
                if b"HTTP" in original_payload:
                    flag_comment = f"<!-- {flag} -->".encode()
                    if b"</html>" in original_payload:
                        # Insert before closing HTML tag
                        new_payload = original_payload.replace(b"</html>", flag_comment + b"</html>")
                    else:
                        # Append to the end
                        new_payload = original_payload + flag_comment
                    
                    # Replace the packet payload
                    packet[Raw].load = new_payload
                    flag_inserted = True
                    logger.info(f"Flag inserted into packet {i}")
                    break
        
        # If no suitable HTTP packet was found, insert the flag into another packet type
        if not flag_inserted:
            logger.info("No suitable HTTP packet found, inserting flag into another packet")
            
            # Choose a packet in the middle of the capture
            target_index = len(packets) // 2
            target_packet = packets[target_index]
            
            # If the packet has a Raw layer, modify it
            if Raw in target_packet:
                original_payload = bytes(target_packet[Raw])
                target_packet[Raw].load = original_payload + f"\n{flag}\n".encode()
            else:
                # Add a Raw layer with the flag
                target_packet = target_packet / Raw(load=f"FLAG:{flag}".encode())
                packets[target_index] = target_packet
            
            logger.info(f"Flag inserted into packet {target_index}")
        
        # Write the modified packets to the output file
        wrpcap(output_pcap, packets)
        logger.info(f"Modified PCAP saved to {output_pcap}")
        return True
    
    except Exception as e:
        logger.error(f"Error processing PCAP file: {e}")
        return False

def main():
    """Main function to create and modify the PCAP file."""
    # Define paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    source_pcap = os.path.join(base_dir, "CTF-capture.pcap")
    capture_dir = os.path.join(base_dir, "capture")
    output_pcap = os.path.join(capture_dir, "capture.pcap")
    
    # Ensure the output directory exists
    os.makedirs(capture_dir, exist_ok=True)
    
    # Check if the source PCAP exists
    if not os.path.exists(source_pcap):
        logger.error(f"Source PCAP file not found at {source_pcap}")
        return False
    
    # Generate the flag
    flag = create_flag()
    
    # Insert the flag into the PCAP
    success = insert_flag_into_pcap(source_pcap, output_pcap, flag)
    
    # If insertion failed, just copy the original file
    if not success:
        logger.warning("Flag insertion failed, copying original PCAP file")
        shutil.copy(source_pcap, output_pcap)
    
    logger.info("PCAP file processing complete")
    return True

if __name__ == "__main__":
    main()