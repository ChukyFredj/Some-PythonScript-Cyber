from scapy.all import IP, ICMP, send, sniff, conf

def envoyer_ping_broadcast(target_ip, broadcast_ip):
    print(f"Envoi de paquets ICMP Echo Request de {broadcast_ip} à {target_ip}")
    icmp_request = IP(src=broadcast_ip, dst=target_ip)/ICMP()
    try:
        send(icmp_request, verbose=1)  # verbose=1 pour plus d'informations
        print("Paquet envoyé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi du paquet: {e}")

def analyser_reponses(packet):
    print("Paquet capturé:", packet.summary())
    if ICMP in packet and packet[ICMP].type == 0:  # ICMP Echo Reply
        src_ip = packet[IP].src
        print(f"Réponse ICMP Echo Reply reçue de {src_ip}")
    else:
        print("Paquet ICMP non identifié reçu")

if __name__ == "__main__":
    target_ip = "192.168.1.118"  # Remplacer par l'adresse IP cible
    broadcast_ip = "192.168.1.255"  # Remplacer par l'adresse IP de broadcast de votre réseau
    # print(conf.route.routes)

    # Utilisez l'interface réseau correcte ici
    interface = "Intel(R) Wi-Fi 6 AX201 160MHz"  # Remplacer par le nom de l'interface réseau trouvée

    # Envoi du paquet ICMP Echo Request
    envoyer_ping_broadcast(target_ip, broadcast_ip)
    
    # Sniffer les paquets ICMP Echo Reply
    print("Analyse des réponses ICMP Echo Reply...")
    try:
        sniff(filter="icmp", prn=analyser_reponses, timeout=60, iface=interface)  # Augmenter le timeout à 60 secondes
        print("Analyse terminée.")
    except Exception as e:
        print(f"Erreur lors du sniffing: {e}")
