from scapy.all import *

def custom_action(packet):

    print(packet.summary())

def sniffer():

    print("Démarrage du sniffer... Capturant 10 paquets")

    sniff(count=10, prn=custom_action, store=False)  

if __name__ == "__main__":
    sniffer()
