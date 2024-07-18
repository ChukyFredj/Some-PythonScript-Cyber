import socket
import time

def scan_ports(ip, port_range):
    open_ports = []
    start_time = time.time()

    for port in range(port_range):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout for socket connection attempt
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()

    end_time = time.time()
    scan_duration = end_time - start_time

    return open_ports, scan_duration

if __name__ == "__main__":
    ip = input("Enter the IP address to scan: ")
    port_range = int(input("Enter the number of ports to scan: "))

    open_ports, scan_duration = scan_ports(ip, port_range)
    print(f"Open ports: {open_ports}")
    print(f"Time taken for the scan: {scan_duration} seconds")
