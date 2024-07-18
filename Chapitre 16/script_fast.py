import socket
import time
import threading

def scan_port(ip, port, open_ports):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    if result == 0:
        open_ports.append(port)
    sock.close()

def scan_ports_fast(ip, port_range):
    open_ports = []
    threads = []
    start_time = time.time()

    for port in range(port_range):
        thread = threading.Thread(target=scan_port, args=(ip, port, open_ports))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    scan_duration = end_time - start_time

    return open_ports, scan_duration


if __name__ == "__main__":
    ip = input("Enter the IP address to scan: ")
    port_range = int(input("Enter the number of ports to scan: "))

    open_ports, scan_duration = scan_ports_fast(ip, port_range)
    print(f"Open ports: {open_ports}")
    print(f"Time taken for the scan: {scan_duration} seconds")
