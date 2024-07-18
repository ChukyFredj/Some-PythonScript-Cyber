import socket
import threading

def client_thread(conn, address):
    print(f"Connected to {address}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Received from {address}: {data.decode()}")
        conn.sendall(data)  # Echo back the received data
    conn.close()

def server():
    host = '127.0.0.1'  # Localhost
    port = 65432  # Port non-privilégié

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server is listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=client_thread, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    server()
