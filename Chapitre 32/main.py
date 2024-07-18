import os
import subprocess
import time
from collections import defaultdict

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande: {e}")

def add_iptables_rule(ip):
    command = f"sudo iptables -A INPUT -s {ip} -j DROP"
    run_command(command)
    print(f"Règle ajoutée pour bloquer {ip}")

def remove_iptables_rule(ip):
    command = f"sudo iptables -D INPUT -s {ip} -j DROP"
    run_command(command)
    print(f"Règle supprimée pour {ip}")

def monitor_log_and_ban(ip_attempts_threshold=5, time_window=60):
    ip_attempts = defaultdict(list)
    banned_ips = set()

    log_file = "/var/log/auth.log"  # Chemin vers le fichier de log à surveiller

    with open(log_file, "r") as file:
        while True:
            line = file.readline()
            if not line:
                time.sleep(1)
                continue

            if "Failed password" in line:
                ip = line.split()[-4]  # Extrait l'IP du log, ajustez selon le format du log

                current_time = time.time()
                ip_attempts[ip].append(current_time)

                # Gardez seulement les tentatives dans la fenêtre de temps spécifiée
                ip_attempts[ip] = [t for t in ip_attempts[ip] if current_time - t <= time_window]

                if len(ip_attempts[ip]) > ip_attempts_threshold:
                    if ip not in banned_ips:
                        add_iptables_rule(ip)
                        banned_ips.add(ip)
                    ip_attempts[ip] = []  # Réinitialise les tentatives après le bannissement

if __name__ == "__main__":
    monitor_log_and_ban()
