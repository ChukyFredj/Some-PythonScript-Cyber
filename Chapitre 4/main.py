from scapy.all import *

def send_icmp_packet(destination):

    packet = IP(dst=destination)/ICMP()


    print("Contenu du paquet ICMP créé :")
    packet.show()


    print(f"Envoi d'un paquet ICMP vers {destination}")
    reply = sr1(packet, timeout=2) 

    if reply:
        print("Réponse reçue :")
        reply.show()
    else:
        print("Aucune réponse reçue.")

def main():
    destination_ip = "8.8.8.8"
    send_icmp_packet(destination_ip)

if __name__ == "__main__":
    main()
