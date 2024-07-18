import nmap
import requests
from bs4 import BeautifulSoup
import sys

def scan_ports(target_ip):
    nm = nmap.PortScanner()
    nm.scan(target_ip, arguments='-sV')
    print(f"[INFO] Scanned {target_ip} for open ports")
    return nm

def get_banners(nm, target_ip):
    banners = []
    for host in nm.all_hosts():
        if host == target_ip:
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                for port in lport:
                    state = nm[host][proto][port]['state']
                    name = nm[host][proto][port]['name']
                    product = nm[host][proto][port]['product']
                    version = nm[host][proto][port]['version']
                    extrainfo = nm[host][proto][port]['extrainfo']
                    banner = f"Port: {port}, State: {state}, Service: {name}, Product: {product}, Version: {version}, Extra Info: {extrainfo}"
                    print(f"[DEBUG] Retrieved banner: {banner}")  # Debugging line
                    banners.append(banner)
    return banners

def save_banners_to_file(banners, filename="banners.txt"):
    with open(filename, 'w') as file:
        for banner in banners:
            file.write(banner + "\n")
    print(f"[INFO] Banners saved to {filename}")

def search_vulnerabilities(banners):
    search_url = "https://www.google.com/search?q="
    headers = {'User-Agent': 'Mozilla/5.0'}

    vulnerabilities = {}
    for banner in banners:
        query = banner.replace(" ", "+")
        url = search_url + query
        print(f"[DEBUG] Searching for vulnerabilities with query: {query}")  # Debugging line
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = [a['href'] for a in soup.find_all('a', href=True)]
        print(f"[DEBUG] Found URLs: {results}")  # Debugging line
        vulnerabilities[banner] = results

    return vulnerabilities

def save_vulnerabilities_to_file(vulnerabilities, filename="vulnerabilities.txt"):
    with open(filename, 'w') as file:
        for banner, urls in vulnerabilities.items():
            file.write(f"{banner}\n")
            for url in urls:
                file.write(f"    {url}\n")
            file.write("\n")
    print(f"[INFO] Vulnerabilities saved to {filename}")

if __name__ == "__main__":
    target_ip = input("Enter the IP address of the target Kali machine: ")

    print("[INFO] Scanning ports...")
    nm = scan_ports(target_ip)

    print("[INFO] Retrieving banners...")
    banners = get_banners(nm, target_ip)
    if not banners:
        print("[ERROR] No banners retrieved. Exiting.")
        sys.exit(1)

    save_banners_to_file(banners)

    print("[INFO] Searching for vulnerabilities...")
    vulnerabilities = search_vulnerabilities(banners)
    if not vulnerabilities:
        print("[ERROR] No vulnerabilities found. Exiting.")
        sys.exit(1)

    save_vulnerabilities_to_file(vulnerabilities)
