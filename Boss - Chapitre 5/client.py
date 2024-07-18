import socket
import sys

def client(message):
    host = '127.0.0.1'  # L'adresse du serveur
    port = 65432  # Le port utilisé par le serveur

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(message.encode())
        data = s.recv(1024)

    print(f"Received: {data.decode()}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client.py <message>")
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
