import os
import logging
import hashlib
import random
import ipaddress
import datetime
import base64
from pathlib import Path
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import (
    Encoding, PrivateFormat, NoEncryption
)
from scapy.all import (
    IP, TCP, UDP, ICMP, Ether, DNS, DNSQR, DNSRR, Raw,
    wrpcap, RandShort, Padding
)

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

def create_rsa_keypair():
    """Create RSA key pair for TLS encryption."""
    # Create key directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    key_dir = os.path.join(base_dir, "key")
    os.makedirs(key_dir, exist_ok=True)
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Get public key
    public_key = private_key.public_key()
    
    # Save private key in PEM format (for Wireshark)
    private_key_path = os.path.join(key_dir, "private.key")
    with open(private_key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=NoEncryption()
        ))
    
    # Save public key in PEM format
    public_key_path = os.path.join(key_dir, "public.key")
    with open(public_key_path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    
    # Create a Wireshark SSL key log file
    keylog_path = os.path.join(key_dir, "sslkeylog.txt")
    with open(keylog_path, "w") as f:
        f.write("# TLS Pre-Master Secret for Wireshark\n")
        # In a real scenario, this would contain the actual TLS secrets
        f.write(f"RSA Session-ID:00000000000000000000000000000000 Master-Key:{os.urandom(48).hex()}\n")
    
    logger.info(f"RSA key pair created and saved to {key_dir}")
    
    return private_key, private_key_path, keylog_path

def create_self_signed_cert(private_key):
    """Create a self-signed certificate for TLS."""
    # Generate a self-signed certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"CTF Challenge"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"capture.example.com"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc)
    ).not_valid_after(
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"capture.example.com")]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    cert_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "key", "cert.pem")
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(Encoding.PEM))
    
    return cert, cert_path

def generate_random_mac():
    """Generate a random MAC address."""
    mac = [random.randint(0x00, 0xff) for _ in range(6)]
    # Set locally administered bit
    mac[0] = (mac[0] & 0xfe) | 0x02
    return ':'.join(map(lambda x: f"{x:02x}", mac))

# First, modify the external_servers list to add a unique flag server
def create_network_config():
    """Create network configuration for the PCAP."""
    home_net = ipaddress.IPv4Network("192.168.1.0/24")
    gateway = str(home_net[1])
    dns_server = str(home_net[2])
    
    # Create a list of devices with realistic parameters
    devices = [
        {
            "name": "Router",
            "ip": gateway,
            "mac": "00:11:22:33:44:55",
            "type": "network",
        },
        {
            "name": "DNS_Server",
            "ip": dns_server,
            "mac": "00:11:22:33:44:56",
            "type": "network",
        },
        {
            "name": "Desktop_PC",
            "ip": str(home_net[10]),
            "mac": generate_random_mac(),
            "type": "computer",
        },
        {
            "name": "Laptop",
            "ip": str(home_net[11]),
            "mac": generate_random_mac(),
            "type": "computer",
        },
        {
            "name": "Smartphone",
            "ip": str(home_net[12]),
            "mac": generate_random_mac(),
            "type": "mobile",
        },
        {
            "name": "SmartTV",
            "ip": str(home_net[20]),
            "mac": generate_random_mac(),
            "type": "iot",
        },
        {
            "name": "SmartSpeaker",
            "ip": str(home_net[21]),
            "mac": generate_random_mac(),
            "type": "iot",
        },
    ]
    
    # External servers
    external_servers = [
        {"name": "Google", "domain": "www.google.com", "ip": "8.8.8.8", "services": ["dns", "http", "https"]},
        {"name": "Facebook", "domain": "www.facebook.com", "ip": "31.13.65.36", "services": ["http", "https"]},
        {"name": "Amazon", "domain": "www.amazon.com", "ip": "52.94.236.248", "services": ["http", "https"]},
        {"name": "Target_Server", "domain": "crazy.fun.com", "ip": "93.184.216.34", "services": ["http", "https"]},
        {"name": "Netflix", "domain": "www.netflix.com", "ip": "44.240.184.200", "services": ["https"]},
        {"name": "Spotify", "domain": "www.spotify.com", "ip": "35.186.224.25", "services": ["https"]},
    ]
    
    #! Flag server
    flag_server = {"name": "Samsung", "domain": "www.samsung.com", "ip": "43.16.227.1", "services": ["https"]}



    return home_net, devices, external_servers, flag_server

def create_pcap_with_scapy(flag, private_key_path):
    """Create a PCAP file with Scapy."""
    # Get network configuration
    home_net, devices, external_servers, flag_server = create_network_config()
    
    # Create directory for output
    base_dir = os.path.dirname(os.path.abspath(__file__))
    capture_dir = os.path.join(base_dir, "capture")
    os.makedirs(capture_dir, exist_ok=True)
    output_pcap = os.path.join(capture_dir, "capture.pcap")
    
    # Initialize the packet list
    packets = []
    flag_packet_position = None
    key_packet_position = None
    
    logger.info("Generating network packets with Scapy...")
    
    # Read private key for DNS TXT record
    with open(private_key_path, "rb") as f:
        private_key_data = f.read().decode('utf-8')
    
    # Special DNS packet with key (will be placed between packets 20-100)
    device = next(d for d in devices if d["name"] == "Desktop_PC")
    
    # Break the key into multiple TXT records (255 chars limit per TXT)
    key_chunks = [private_key_data[i:i+240] for i in range(0, len(private_key_data), 240)]
    logger.info(f"Split RSA key into {len(key_chunks)} chunks for DNS TXT records")
    
    # Create DNS query for the key
    dns_key_query = (
        Ether(src=device["mac"], dst="00:11:22:33:44:55") /
        IP(src=device["ip"], dst="8.8.8.8") /
        UDP(sport=RandShort(), dport=53) /
        DNS(rd=1, qd=DNSQR(qname="HereIsTheKey.local"))
    )
    
    # Create DNS response with all key chunks in multiple TXT records
    dns_rrs = []
    for i, chunk in enumerate(key_chunks):
        dns_rrs.append(
            DNSRR(
                rrname="HereIsTheKey.local",
                ttl=86400,
                type="TXT",
                rdata=chunk
            )
        )
    
    dns_key_response = (
        Ether(src="00:11:22:33:44:55", dst=device["mac"]) /
        IP(src="8.8.8.8", dst=device["ip"]) /
        UDP(sport=53, dport=dns_key_query[UDP].sport) /
        DNS(
            id=dns_key_query[DNS].id,
            qd=dns_key_query[DNS].qd,
            aa=1,
            qr=1,
            an=dns_rrs  # Use all TXT records
        )
    )
    
    # Save references to special packets
    key_query_ref = dns_key_query
    key_response_ref = dns_key_response
    
    # Generate standard DNS traffic (5000 packets = 2500 queries + 2500 responses)
    logger.info("Generating DNS traffic...")
    for _ in range(2500):
        device = random.choice(devices)
        server = random.choice(external_servers)
        
        # DNS query
        dns_query = (
            Ether(src=device["mac"], dst="00:11:22:33:44:55") /
            IP(src=device["ip"], dst="8.8.8.8") /
            UDP(sport=RandShort(), dport=53) /
            DNS(rd=1, qd=DNSQR(qname=server["domain"]))
        )
        
        # DNS response
        dns_response = (
            Ether(src="00:11:22:33:44:55", dst=device["mac"]) /
            IP(src="8.8.8.8", dst=device["ip"]) /
            UDP(sport=53, dport=dns_query[UDP].sport) /
            DNS(
                id=dns_query[DNS].id,
                qd=dns_query[DNS].qd,
                aa=1,
                qr=1,
                an=DNSRR(
                    rrname=server["domain"],
                    ttl=86400,
                    type="A",
                    rdata=server["ip"]
                )
            )
        )
        
        packets.append(dns_query)
        packets.append(dns_response)
    
    # Generate HTTP traffic (5000 packets)
    logger.info("Generating HTTP traffic...")
    for _ in range(1000):
        device = random.choice([d for d in devices if d["type"] in ["computer", "mobile"]])
        server = random.choice(external_servers)
        
        # TCP handshake + HTTP request/response (5 packets per iteration)
        syn = (
            Ether(src=device["mac"], dst="00:11:22:33:44:55") /
            IP(src=device["ip"], dst=server["ip"]) /
            TCP(sport=RandShort(), dport=80, flags="S")
        )
        
        syn_ack = (
            Ether(src="00:11:22:33:44:55", dst=device["mac"]) /
            IP(src=server["ip"], dst=device["ip"]) /
            TCP(sport=80, dport=syn[TCP].sport, flags="SA", seq=1000, ack=syn[TCP].seq + 1)
        )
        
        ack = (
            Ether(src=device["mac"], dst="00:11:22:33:44:55") /
            IP(src=device["ip"], dst=server["ip"]) /
            TCP(sport=syn[TCP].sport, dport=80, flags="A", seq=syn[TCP].seq + 1, ack=syn_ack[TCP].seq + 1)
        )
        
        http_req = (
            Ether(src=device["mac"], dst="00:11:22:33:44:55") /
            IP(src=device["ip"], dst=server["ip"]) /
            TCP(sport=syn[TCP].sport, dport=80, flags="PA", seq=ack[TCP].seq, ack=ack[TCP].ack) /
            Raw(load=f"GET / HTTP/1.1\r\nHost: {server['domain']}\r\nUser-Agent: Mozilla/5.0\r\nAccept: text/html\r\n\r\n")
        )
        
        http_resp = (
            Ether(src="00:11:22:33:44:55", dst=device["mac"]) /
            IP(src=server["ip"], dst=device["ip"]) /
            TCP(sport=80, dport=http_req[TCP].sport, flags="PA", seq=syn_ack[TCP].seq + 1, ack=http_req[TCP].seq + len(http_req[Raw])) /
            Raw(load="HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body>Example page</body></html>")
        )
        
        packets.extend([syn, syn_ack, ack, http_req, http_resp])
    
    # Generate HTTPS traffic with flag
    logger.info("Generating HTTPS traffic with embedded flag...")
    
    # Choose a specific device and server for flag
    target_device = next(d for d in devices if d["name"] == "Desktop_PC")
    target_server = flag_server
    
    # HTTPS traffic with flag (12 packets)
    syn = (
        Ether(src=target_device["mac"], dst="00:11:22:33:44:55") /
        IP(src=target_device["ip"], dst=target_server["ip"]) /
        TCP(sport=RandShort(), dport=443, flags="S")
    )
    
    syn_ack = (
        Ether(src="00:11:22:33:44:55", dst=target_device["mac"]) /
        IP(src=target_server["ip"], dst=target_device["ip"]) /
        TCP(sport=443, dport=syn[TCP].sport, flags="SA", seq=5000, ack=syn[TCP].seq + 1)
    )
    
    ack = (
        Ether(src=target_device["mac"], dst="00:11:22:33:44:55") /
        IP(src=target_device["ip"], dst=target_server["ip"]) /
        TCP(sport=syn[TCP].sport, dport=443, flags="A", seq=syn[TCP].seq + 1, ack=syn_ack[TCP].seq + 1)
    )
    
    client_hello = (
        Ether(src=target_device["mac"], dst="00:11:22:33:44:55") /
        IP(src=target_device["ip"], dst=target_server["ip"]) /
        TCP(sport=syn[TCP].sport, dport=443, flags="PA", seq=ack[TCP].seq, ack=ack[TCP].ack) /
        Raw(load=b"\x16\x03\x01" + os.urandom(200))
    )
    
    server_hello = (
        Ether(src="00:11:22:33:44:55", dst=target_device["mac"]) /
        IP(src=target_server["ip"], dst=target_device["ip"]) /
        TCP(sport=443, dport=client_hello[TCP].sport, flags="PA", seq=syn_ack[TCP].seq + 1, ack=client_hello[TCP].seq + len(client_hello[Raw])) /
        Raw(load=b"\x16\x03\x03" + os.urandom(300))
    )
    
    client_key_exchange = (
        Ether(src=target_device["mac"], dst="00:11:22:33:44:55") /
        IP(src=target_device["ip"], dst=target_server["ip"]) /
        TCP(sport=syn[TCP].sport, dport=443, flags="PA", seq=client_hello[TCP].seq + len(client_hello[Raw]), ack=server_hello[TCP].seq + len(server_hello[Raw])) /
        Raw(load=b"\x16\x03\x03" + os.urandom(150))
    )
    
    server_finished = (
        Ether(src="00:11:22:33:44:55", dst=target_device["mac"]) /
        IP(src=target_server["ip"], dst=target_device["ip"]) /
        TCP(sport=443, dport=client_key_exchange[TCP].sport, flags="PA", seq=server_hello[TCP].seq + len(server_hello[Raw]), ack=client_key_exchange[TCP].seq + len(client_key_exchange[Raw])) /
        Raw(load=b"\x14\x03\x03" + os.urandom(30))
    )
    
    encrypted_request = (
        Ether(src=target_device["mac"], dst="00:11:22:33:44:55") /
        IP(src=target_device["ip"], dst=target_server["ip"]) /
        TCP(sport=syn[TCP].sport, dport=443, flags="PA", seq=client_key_exchange[TCP].seq + len(client_key_exchange[Raw]), ack=server_finished[TCP].seq + len(server_finished[Raw])) /
        Raw(load=b"\x17\x03\x03" + os.urandom(200))
    )

    unique_identifier = "R3@&hs0§"
    
    # Create a realistic HTTP response with the flag
    http_content = f"""HTTP/1.1 200 OK
Server: nginx/1.19.0
Date: {datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}
Content-Type: text/html
Content-Length: 256
Connection: close

<html>
<head><title>Secret Flag Page</title></head>
<body>
<!-- The flag is: {flag} -->
<h1>Welcome to the Secret Page</h1>
<p>This page contains sensitive information.</p>
</body>
</html>
"""

    # Properly simulate TLS encryption by only showing encrypted bytes
    unique_identifier = "R3@&hs0"

    encrypted_data = b"\x17\x03\x03" + b"\x00\xFF" + unique_identifier.encode() + b" " + os.urandom(len(http_content) + 50)

    encrypted_response = (
        Ether(src="00:11:22:33:44:55", dst=target_device["mac"]) /
        IP(src=target_server["ip"], dst=target_device["ip"]) /
        TCP(sport=443, dport=encrypted_request[TCP].sport, flags="PA", seq=server_finished[TCP].seq + len(server_finished[Raw]), ack=encrypted_request[TCP].seq + len(encrypted_request[Raw])) /
        Raw(load=encrypted_data)
    )
    
    flag_identifier = {
        "server_ip": target_server["ip"],
        "client_ip": target_device["ip"],
        "server_port": 443,
        "client_port": encrypted_request[TCP].sport,
        "seq_num": encrypted_response[TCP].seq
    }
    
    fin_ack = (
        Ether(src=target_device["mac"], dst="00:11:22:33:44:55") /
        IP(src=target_device["ip"], dst=target_server["ip"]) /
        TCP(sport=syn[TCP].sport, dport=443, flags="FA", seq=encrypted_request[TCP].seq + len(encrypted_request[Raw]), ack=encrypted_response[TCP].seq + len(encrypted_response[Raw]))
    )
    
    fin_ack_response = (
        Ether(src="00:11:22:33:44:55", dst=target_device["mac"]) /
        IP(src=target_server["ip"], dst=target_device["ip"]) /
        TCP(sport=443, dport=fin_ack[TCP].sport, flags="FA", seq=encrypted_response[TCP].seq + len(encrypted_response[Raw]), ack=fin_ack[TCP].seq + 1)
    )
    
    final_ack = (
        Ether(src=target_device["mac"], dst="00:11:22:33:44:55") /
        IP(src=target_device["ip"], dst=target_server["ip"]) /
        TCP(sport=syn[TCP].sport, dport=443, flags="A", seq=fin_ack[TCP].seq + 1, ack=fin_ack_response[TCP].seq + 1)
    )
    
    packets.extend([syn, syn_ack, ack, client_hello, server_hello, client_key_exchange, 
                   server_finished, encrypted_request, encrypted_response, fin_ack, 
                   fin_ack_response, final_ack])
    
    # Generate additional HTTPS sessions (8 packets per session)
    logger.info("Generating additional HTTPS traffic...")
    for _ in range(1500):
        device = random.choice([d for d in devices if d["type"] in ["computer", "mobile"]])
        server = random.choice(external_servers)
        
        syn = (
            Ether(src=device["mac"], dst="00:11:22:33:44:55") /
            IP(src=device["ip"], dst=server["ip"]) /
            TCP(sport=RandShort(), dport=443, flags="S")
        )
        
        syn_ack = (
            Ether(src="00:11:22:33:44:55", dst=device["mac"]) /
            IP(src=server["ip"], dst=device["ip"]) /
            TCP(sport=443, dport=syn[TCP].sport, flags="SA", seq=random.randint(1000, 9000), ack=syn[TCP].seq + 1)
        )
        
        ack = (
            Ether(src=device["mac"], dst="00:11:22:33:44:55") /
            IP(src=device["ip"], dst=server["ip"]) /
            TCP(sport=syn[TCP].sport, dport=443, flags="A", seq=syn[TCP].seq + 1, ack=syn_ack[TCP].seq + 1)
        )
        
        client_data = (
            Ether(src=device["mac"], dst="00:11:22:33:44:55") /
            IP(src=device["ip"], dst=server["ip"]) /
            TCP(sport=syn[TCP].sport, dport=443, flags="PA", seq=ack[TCP].seq, ack=ack[TCP].ack) /
            Raw(load=b"\x17\x03\x03" + os.urandom(random.randint(50, 150)))
        )
        
        server_data = (
            Ether(src="00:11:22:33:44:55", dst=device["mac"]) /
            IP(src=server["ip"], dst=device["ip"]) /
            TCP(sport=443, dport=client_data[TCP].sport, flags="PA", seq=syn_ack[TCP].seq + 1, ack=client_data[TCP].seq + len(client_data[Raw])) /
            Raw(load=b"\x17\x03\x03" + os.urandom(random.randint(100, 300)))
        )
        
        fin = (
            Ether(src=device["mac"], dst="00:11:22:33:44:55") /
            IP(src=device["ip"], dst=server["ip"]) /
            TCP(sport=syn[TCP].sport, dport=443, flags="FA", seq=client_data[TCP].seq + len(client_data[Raw]), ack=server_data[TCP].seq + len(server_data[Raw]))
        )
        
        fin_ack = (
            Ether(src="00:11:22:33:44:55", dst=device["mac"]) /
            IP(src=server["ip"], dst=device["ip"]) /
            TCP(sport=443, dport=fin[TCP].sport, flags="FA", seq=server_data[TCP].seq + len(server_data[Raw]), ack=fin[TCP].seq + 1)
        )
        
        last_ack = (
            Ether(src=device["mac"], dst="00:11:22:33:44:55") /
            IP(src=device["ip"], dst=server["ip"]) /
            TCP(sport=syn[TCP].sport, dport=443, flags="A", seq=fin[TCP].seq + 1, ack=fin_ack[TCP].seq + 1)
        )
        
        packets.extend([syn, syn_ack, ack, client_data, server_data, fin, fin_ack, last_ack])
    
    # Generate ICMP traffic
    logger.info("Generating ICMP traffic...")
    for _ in range(1000):
        device1 = random.choice(devices)
        device2 = random.choice(devices)
        
        echo_request = (
            Ether(src=device1["mac"], dst="00:11:22:33:44:55") /
            IP(src=device1["ip"], dst=device2["ip"]) /
            ICMP(type=8, code=0, id=random.randint(1, 65535), seq=1) /
            Raw(load=os.urandom(56))
        )
        
        echo_reply = (
            Ether(src="00:11:22:33:44:55", dst=device1["mac"]) /
            IP(src=device2["ip"], dst=device1["ip"]) /
            ICMP(type=0, code=0, id=echo_request[ICMP].id, seq=1) /
            echo_request[Raw]
        )
        
        packets.extend([echo_request, echo_reply])
    
    # Remove the key packets from the original packet set
    all_packets = []
    for p in packets:
        if p != key_query_ref and p != key_response_ref:
            all_packets.append(p)
    
    # Insert the key packets at a fixed position
    key_position = random.randint(20, 80)
    logger.info(f"Inserting key DNS packets at positions {key_position} and {key_position+1}")
    all_packets = all_packets[:key_position] + [key_query_ref, key_response_ref] + all_packets[key_position:]
    
    # Shuffle all packets 
    random.shuffle(all_packets)
    
    # Find the exact positions after shuffling
    key_packet_position = None
    key_response_position = None
    flag_packet_position = None
    
    for i, packet in enumerate(all_packets):
        # Find the DNS query packet
        if UDP in packet and DNS in packet and packet.haslayer(DNSQR):
            if hasattr(packet[DNSQR], 'qname'):
                qname = packet[DNSQR].qname
                if isinstance(qname, bytes):
                    qname = qname.decode('utf-8', errors='ignore')
                if "HereIsTheKey.local" in qname:
                    key_packet_position = i + 1  # Add +1 to the position for logging
                    logger.info(f"Found DNS query for key at packet #{i+1}")
        
        # Find the DNS response packet
        if UDP in packet and DNS in packet and packet.haslayer(DNSRR):
            for j in range(len(packet[DNS].an)):
                if hasattr(packet[DNS].an[j], 'rrname'):
                    rrname = packet[DNS].an[j].rrname
                    if isinstance(rrname, bytes):
                        rrname = rrname.decode('utf-8', errors='ignore')
                    if "HereIsTheKey.local" in rrname:
                        key_response_position = i + 1  # Add +1 to the position for logging
                        logger.info(f"Found DNS response with {len(packet[DNS].an)} TXT records at packet #{i+1}")
                        break
        
        if IP in packet and TCP in packet and Raw in packet:
                if packet[Raw].load.startswith(b"\x17\x03\x03") and unique_identifier.encode() in packet[Raw].load: flag_packet_position = i + 1
                logger.info(f"Found TLS packet with flag at packet #{i+1}")
                break
    

    # Write the packets to the PCAP file
    total_packets = len(all_packets)
    logger.info(f"Writing {total_packets} packets to PCAP file...")
    wrpcap(output_pcap, all_packets)
    
    logger.info(f"Successfully created PCAP with {total_packets} packets at {output_pcap}")
    logger.info(f"Important packet information:")
    logger.info(f"- RSA private key is in DNS response for 'HereIsTheKey.local' at packet #{key_response_position}")
    logger.info(f"- Flag is embedded in HTTPS traffic at packet #{flag_packet_position}")
    
    return output_pcap

def create_pcap_with_flag():
    """Main function to create the PCAP file with embedded flag."""
    # Create the flag
    flag = create_flag()
    
    # Generate RSA key pair for TLS
    private_key, private_key_path, keylog_path = create_rsa_keypair()
    
    # Create self-signed certificate
    certificate, cert_path = create_self_signed_cert(private_key)
    
    try:
        # Generate PCAP with Scapy - pass the private_key_path
        output_pcap = create_pcap_with_scapy(flag, private_key_path)
        
        # Create NSS key format file for Wireshark
        base_dir = os.path.dirname(os.path.abspath(__file__))
        key_dir = os.path.join(base_dir, "key")
        nss_key_path = os.path.join(key_dir, "nss_keys.txt")
        
        with open(nss_key_path, "w") as f:
            f.write("# TLS Pre-Master Secret for Wireshark\n")
            f.write(f"RSA,{private_key_path}\n")
        
        # Final PCAP location
        capture_dir = os.path.join(base_dir, "capture")
        output_pcap = os.path.join(capture_dir, "capture.pcap")
        
        if os.path.exists(output_pcap):
            logger.info(f"Successfully created PCAP with flag at {output_pcap}")
            logger.info(f"TLS keys saved in {key_dir}")
            return True
        else:
            logger.error("PCAP file was not created properly")
            return False
    
    except Exception as e:
        logger.error(f"Error creating PCAP: {e}")
        return False
    
if __name__ == "__main__":
    create_pcap_with_flag()