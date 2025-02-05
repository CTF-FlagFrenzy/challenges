import os
from scapy.all import IP, UDP, DNS, DNSQR, TCP, Raw, ARP, wrpcap

# Erstelle das Verzeichnis, falls es nicht existiert
os.makedirs("capture", exist_ok=True)

# Erstelle eine Liste von Paketen
packets = []

# Füge DNS-Pakete hinzu
for i in range(25):
    dns_packet = IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname="example.com"))
    packets.append(dns_packet)

# Füge HTTP-Pakete hinzu
for i in range(25):
    http_packet = IP(dst="93.184.216.34")/TCP(dport=80)/Raw(load="GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
    packets.append(http_packet)

# Füge HTTPS-Pakete hinzu
for i in range(25):
    https_packet = IP(dst="93.184.216.34")/TCP(dport=443)/Raw(load="GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
    packets.append(https_packet)

# Füge ARP-Pakete hinzu
for i in range(25):
    arp_packet = ARP(pdst="192.168.1.1")
    packets.append(arp_packet)

# Speichere alle Pakete in einer PCAP-Datei
wrpcap("capture/capture.pcap", packets)

print("PCAP-Datei mit DNS-, HTTP-, HTTPS- und ARP-Paketen erstellt.")