# ============================================
# Port Scanner
# Built by: Kainat
# Project 3 — Cybersecurity Portfolio
# ⚠️ Only scan YOUR OWN network or localhost!
# ============================================

import socket
import datetime

# ---- COMMON PORTS DICTIONARY ----
# These are the most important ports to know
COMMON_PORTS = {
    21:   "FTP (File Transfer)",
    22:   "SSH (Secure Shell)",
    23:   "Telnet (Unsecure Remote)",
    25:   "SMTP (Email Sending)",
    53:   "DNS (Domain Name System)",
    80:   "HTTP (Website)",
    110:  "POP3 (Email Receiving)",
    135:  "RPC (Windows)",
    139:  "NetBIOS (Windows Sharing)",
    143:  "IMAP (Email)",
    443:  "HTTPS (Secure Website)",
    445:  "SMB (Windows File Sharing)",
    3306: "MySQL (Database)",
    3389: "RDP (Remote Desktop)",
    5432: "PostgreSQL (Database)",
    5900: "VNC (Remote Desktop)",
    8080: "HTTP Alternative",
    8443: "HTTPS Alternative",
}

# ---- SCAN A SINGLE PORT ----
def scan_port(target, port):
    """Try to connect to a port — if it connects, port is OPEN"""
    try:
        # Create a socket (like a phone call to a port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # wait max 1 second

        # Try to connect
        result = sock.connect_ex((target, port))
        sock.close()

        if result == 0:
            return True  # Port is OPEN
        else:
            return False  # Port is CLOSED
    except:
        return False

# ---- GET SERVICE NAME ----
def get_service(port):
    """Return what service runs on this port"""
    if port in COMMON_PORTS:
        return COMMON_PORTS[port]
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown Service"

# ---- RISK LEVEL ----
def get_risk(port):
    """Return risk level for open port"""
    high_risk = [21, 23, 135, 139, 445, 3389, 5900]
    medium_risk = [25, 110, 143, 3306, 5432, 8080]

    if port in high_risk:
        return "🔴 HIGH RISK"
    elif port in medium_risk:
        return "🟡 MEDIUM RISK"
    else:
        return "🟢 LOW RISK"

# ---- MAIN SCANNER ----
def scan_target(target, start_port, end_port):
    """Scan a range of ports on a target"""

    print("\n" + "=" * 60)
    print("   PORT SCANNER — by Kainat")
    print("=" * 60)
    print(f"   Target     : {target}")
    print(f"   Port Range : {start_port} - {end_port}")
    print(f"   Started    : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("\n🔍 Scanning ports... please wait...\n")

    open_ports = []

    # Scan each port one by one
    for port in range(start_port, end_port + 1):
        if scan_port(target, port):
            service = get_service(port)
            risk = get_risk(port)
            open_ports.append((port, service, risk))
            print(f"   [OPEN] Port {port:5d} → {service:30s} {risk}")

    # Summary
    print("\n" + "=" * 60)
    print(f"   SCAN COMPLETE!")
    print(f"   Open ports found: {len(open_ports)}")
    print("=" * 60)

    if open_ports:
        print("\n⚠️  SECURITY ADVICE:")
        print("-" * 40)
        for port, service, risk in open_ports:
            if "HIGH" in risk:
                print(f"   → Port {port} ({service}) is HIGH RISK — consider closing it!")
            elif "MEDIUM" in risk:
                print(f"   → Port {port} ({service}) — monitor this port carefully")
    else:
        print("\n✅ No open ports found — target looks secure!")

    print("=" * 60 + "\n")

# ---- RUN THE PROGRAM ----
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("   🔍 PORT SCANNER by Kainat")
    print("   ⚠️  Only scan YOUR OWN systems!")
    print("=" * 60)

    # Get target
    target = input("\nEnter target IP (press Enter for localhost): ").strip()
    if not target:
        target = "127.0.0.1"  # default to your own computer

    # Get port range
    print("\nPort range options:")
    print("   1 → Quick scan (1-100 common ports)")
    print("   2 → Standard scan (1-1000 ports)")
    print("   3 → Custom range")

    choice = input("\nChoose option (1/2/3): ").strip()

    if choice == "1":
        start_port, end_port = 1, 100
    elif choice == "2":
        start_port, end_port = 1, 1000
    elif choice == "3":
        start_port = int(input("Start port: "))
        end_port = int(input("End port: "))
    else:
        start_port, end_port = 1, 100

    # Run scan
    try:
        scan_target(target, start_port, end_port)
    except KeyboardInterrupt:
        print("\n\n⚠️  Scan stopped by user!\n")
    except socket.gaierror:
        print("\n❌ Could not resolve target — check the IP address!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
