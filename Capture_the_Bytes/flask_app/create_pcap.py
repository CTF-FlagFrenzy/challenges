import hashlib
import logging
import os
import shutil
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

def create_wireshark_key():
    """Create the Wireshark key file for TLS decryption."""
    # Create key directory in flask_app
    base_dir = os.path.dirname(os.path.abspath(__file__))
    key_dir = os.path.join(base_dir, "key")
    os.makedirs(key_dir, exist_ok=True)
    
    # Define path for the Wireshark key file
    wireshark_key_path = os.path.join(key_dir, "tls_key.log")
    
    # Generate a simple key log file in the format Wireshark expects
    with open(wireshark_key_path, "w") as f:
        # Format: CLIENT_RANDOM <client_random> <master_secret>
        client_random = "2b1f5c76f9a3b2c4d5e6f78901a2b3c4d5e6f7890a1b2c3d4e5f67890a1b2c3d"
        master_secret = "9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b"
        f.write(f"CLIENT_RANDOM {client_random} {master_secret}")
    
    logger.info(f"Generated Wireshark TLS key file at {wireshark_key_path}")
    return wireshark_key_path

def insert_flag_into_pcap(input_pcap, output_pcap, flag):
    """Insert the flag into a specific packet in the PCAP file."""
    try:
        # Create the Wireshark key file first
        wireshark_key_path = create_wireshark_key()
        
        # Read the original PCAP file
        packets = rdpcap(input_pcap)
        logger.info(f"Loaded {len(packets)} packets from {input_pcap}")
        
        if len(packets) < 1000:
            logger.warning("PCAP file has fewer packets than expected")
        
        # Convert PacketList to a list to allow modifications
        packets_list = [p for p in packets]
        
        # Find HTTPS packets (TCP port 443)
        flag_inserted = False
        https_packets = []
        
        for i, packet in enumerate(packets):
            if IP in packet and TCP in packet and (packet[TCP].dport == 443 or packet[TCP].sport == 443):
                https_packets.append((i, packet))
        
        if https_packets:
            logger.info(f"Found {len(https_packets)} HTTPS packets")
            
            # Choose a packet in the middle of the HTTPS sequence
            target_idx = len(https_packets) // 2
            packet_idx, target_packet = https_packets[target_idx]
            
            # Insert flag into an encrypted payload
            if Raw in target_packet:
                # Modify existing payload
                original_payload = bytes(target_packet[Raw])
                modified_payload = original_payload + f"\nEncrypted-Flag: {flag}\n".encode()
                new_packet = target_packet.copy()
                new_packet[Raw].load = modified_payload
                packets_list[packet_idx] = new_packet
            else:
                # Add a new Raw payload
                new_packet = target_packet.copy() / Raw(load=f"Encrypted-Flag: {flag}".encode())
                packets_list[packet_idx] = new_packet
            
            flag_inserted = True
            logger.info(f"Flag inserted into HTTPS packet {packet_idx}")

        # If no HTTPS packets found or flag insertion failed, try HTTP packets
        if not flag_inserted:
            logger.info("Trying HTTP packets...")
            
            for i, packet in enumerate(packets_list):
                if IP in packet and TCP in packet and packet[TCP].dport == 80 and Raw in packet:
                    # Get the original payload
                    original_payload = bytes(packet[Raw])
                    
                    # Create a new payload with our flag
                    if b"HTTP" in original_payload:
                        flag_comment = f"<!-- Flag: {flag} -->".encode()
                        if b"</html>" in original_payload:
                            # Insert before closing HTML tag
                            new_payload = original_payload.replace(b"</html>", flag_comment + b"</html>")
                        else:
                            # Append to the end
                            new_payload = original_payload + flag_comment
                        
                        # Replace the packet payload
                        new_packet = packet.copy()
                        new_packet[Raw].load = new_payload
                        packets_list[i] = new_packet
                        flag_inserted = True
                        logger.info(f"Flag inserted into HTTP packet {i}")
                        break
        
        # If still no suitable packet found, insert the flag into another packet type
        if not flag_inserted:
            logger.info("No suitable HTTP/HTTPS packet found, inserting flag into another packet")
            
            # Choose a packet in the middle of the capture
            target_index = len(packets_list) // 2
            target_packet = packets_list[target_index]
            
            # If the packet has a Raw layer, modify it
            if Raw in target_packet:
                original_payload = bytes(target_packet[Raw])
                new_packet = target_packet.copy()
                new_packet[Raw].load = original_payload + f"\n{flag}\n".encode()
                packets_list[target_index] = new_packet
            else:
                # Add a Raw layer with the flag
                new_packet = target_packet.copy() / Raw(load=f"FLAG:{flag}".encode())
                packets_list[target_index] = new_packet
            
            logger.info(f"Flag inserted into packet {target_index}")
        
        # Write the modified packets to the output file
        wrpcap(output_pcap, packets_list)
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