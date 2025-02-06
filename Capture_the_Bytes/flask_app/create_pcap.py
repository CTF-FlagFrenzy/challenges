import scapy.all as scapy
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Generate an RSA key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

# Serialize the keys
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

logging.info("Generated RSA key pair")

# Save the private key to a file
key_dir = "key"
if not os.path.exists(key_dir):
    os.makedirs(key_dir)

private_key_file = os.path.join(key_dir, "private_key.pem")
with open(private_key_file, "wb") as f:
    f.write(private_pem)

logging.info(f"Private key saved to {private_key_file}")

# Load the pcap file
try:
    packets = scapy.rdpcap("CTF-Capture.pcap")
    logging.info("Successfully loaded CTF-Capture.pcap")
except FileNotFoundError:
    logging.error("Error: CTF-Capture.pcap not found.")
    exit()

# Craft the HTTPS packet with the challenge
challenge_data = b"This is the CTF challenge data!"

# Encrypt the challenge data with the public key
encrypted_data = public_key.encrypt(
    challenge_data,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
logging.info("Challenge data encrypted with RSA public key")

# Create a TLS/SSL record with the encrypted data as application data
tls_record = scapy.TLS(version="TLS_1_2", content_type="application_data", length=len(encrypted_data), data=encrypted_data)

# Create a TCP layer
tcp_layer = scapy.TCP(dport=443, sport=12345)  # Standard HTTPS port is 443

# Create an IP layer
ip_layer = scapy.IP(dst="10.0.0.1", src="10.0.0.2")  # Replace with appropriate IP addresses

# Create an Ethernet layer
ethernet_layer = scapy.Ether(dst="00:11:22:33:44:55", src="66:77:88:99:aa:bb")  # Replace with appropriate MAC addresses

# Combine the layers to form the packet
https_packet = ethernet_layer / ip_layer / tcp_layer / tls_record
logging.info("HTTPS packet crafted")

# Add the crafted packet to the list of packets
packets.append(https_packet)
packet_number = len(packets)
logging.info(f"HTTPS packet appended to packet list as packet number: {packet_number}")

# Write the modified packet list back to a new pcap file
scapy.wrpcap("capture/modified_capture.pcap", packets)
logging.info("Modified packet list written to modified_capture.pcap")