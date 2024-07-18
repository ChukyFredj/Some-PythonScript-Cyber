import re
import subprocess
import sys

def validate_mac_address(mac):
    """ Validate MAC address format """
    if re.match(r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$", mac):
        return True
    else:
        return False

def get_network_interfaces():
    """ Get a list of available network interfaces """
    result = subprocess.run(["ip", "link", "show"], capture_output=True, text=True)
    interfaces = re.findall(r"^\d+: (\w+):", result.stdout, re.MULTILINE)
    return interfaces

def change_mac_address(interface, new_mac):
    """ Change the MAC address of the given interface """
    try:
        subprocess.run(["sudo", "ifconfig", interface, "down"], check=True)
        subprocess.run(["sudo", "ifconfig", interface, "hw", "ether", new_mac], check=True)
        subprocess.run(["sudo", "ifconfig", interface, "up"], check=True)
        print(f"[INFO] MAC address for {interface} changed to {new_mac}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to change MAC address: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python change_mac.py <interface> <new_mac>")
        sys.exit(1)

    interface = sys.argv[1]
    new_mac = sys.argv[2]

    if not validate_mac_address(new_mac):
        print("[ERROR] Invalid MAC address format. Use format XX:XX:XX:XX:XX:XX.")
        sys.exit(1)

    interfaces = get_network_interfaces()
    if interface not in interfaces:
        print(f"[ERROR] Interface {interface} not found. Available interfaces: {', '.join(interfaces)}")
        sys.exit(1)

    change_mac_address(interface, new_mac)
