from scapy.all import ARP, Ether, srp
import sys

def get_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc if answered_list else None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_mac.py <IP>")
        sys.exit(1)

    ip = sys.argv[1]
    mac = get_mac(ip)

    if mac:
        print(f"L'adresse MAC de {ip} est {mac}")
    else:
        print(f"Impossible de récupérer l'adresse MAC de {ip}")
