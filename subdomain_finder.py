# ============================================
# Subdomain Finder
# Built by: Kainat
# Project 4 — Cybersecurity Portfolio
# ⚠️ Only scan websites you have permission to test!
# ============================================

import socket
import datetime

# ---- WORDLIST ----
# Common subdomain names to check
SUBDOMAINS = [
    "www", "mail", "ftp", "admin", "blog", "shop",
    "api", "dev", "test", "staging", "portal", "app",
    "secure", "vpn", "remote", "server", "ns1", "ns2",
    "smtp", "pop", "imap", "webmail", "cpanel", "whm",
    "forum", "help", "support", "chat", "cdn", "media",
    "images", "static", "login", "register", "signup",
    "dashboard", "panel", "backend", "frontend", "old",
    "new", "beta", "alpha", "demo", "docs", "wiki",
    "backup", "db", "database", "mysql", "sql", "ssh",
    "git", "svn", "jenkins", "ci", "monitor", "status",
    "analytics", "tracking", "ads", "search", "mobile",
    "wap", "cloud", "files", "download", "upload", "store"
]

# ---- CHECK SUBDOMAIN ----
def check_subdomain(domain, subdomain):
    """Check if a subdomain exists using DNS lookup"""
    full_domain = f"{subdomain}.{domain}"
    try:
        # Try to get IP address of subdomain
        ip = socket.gethostbyname(full_domain)
        return True, full_domain, ip
    except socket.gaierror:
        return False, full_domain, None

# ---- RISK ASSESSMENT ----
def get_risk(subdomain):
    """Check if subdomain is potentially risky"""
    high_risk = ["admin", "backend", "cpanel", "whm", "db",
                 "database", "mysql", "sql", "ssh", "panel",
                 "backup", "old", "test", "staging", "dev"]
    medium_risk = ["api", "login", "register", "dashboard",
                   "portal", "remote", "vpn", "git", "jenkins"]

    if subdomain in high_risk:
        return "🔴 HIGH RISK"
    elif subdomain in medium_risk:
        return "🟡 MEDIUM RISK"
    else:
        return "🟢 LOW RISK"

# ---- MAIN SCANNER ----
def find_subdomains(domain):
    """Find all subdomains for a given domain"""

    print("\n" + "=" * 60)
    print("   SUBDOMAIN FINDER — by Kainat")
    print("=" * 60)
    print(f"   Target  : {domain}")
    print(f"   Checking: {len(SUBDOMAINS)} possible subdomains")
    print(f"   Started : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("\n🔍 Scanning subdomains... please wait...\n")

    found_subdomains = []

    for subdomain in SUBDOMAINS:
        exists, full_domain, ip = check_subdomain(domain, subdomain)
        if exists:
            risk = get_risk(subdomain)
            found_subdomains.append((full_domain, ip, risk))
            print(f"   [FOUND] {full_domain:40s} → {ip:15s} {risk}")

    # Summary
    print("\n" + "=" * 60)
    print(f"   SCAN COMPLETE!")
    print(f"   Found: {len(found_subdomains)} subdomains")
    print("=" * 60)

    if found_subdomains:
        print("\n⚠️  SECURITY ADVICE:")
        print("-" * 40)
        for full_domain, ip, risk in found_subdomains:
            if "HIGH" in risk:
                print(f"   → {full_domain} is HIGH RISK — secure or remove!")
            elif "MEDIUM" in risk:
                print(f"   → {full_domain} — monitor carefully")
    else:
        print("\n✅ No subdomains found!")

    print("=" * 60 + "\n")
    return found_subdomains

# ---- RUN THE PROGRAM ----
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("   🔍 SUBDOMAIN FINDER by Kainat")
    print("   ⚠️  Only scan with permission!")
    print("=" * 60)

    domain = input("\nEnter target domain (e.g. google.com): ").strip()

    if not domain:
        print("❌ Please enter a domain!")
    else:
        # Remove http:// or https:// if included
        domain = domain.replace("https://", "").replace("http://", "").strip("/")

        try:
            find_subdomains(domain)
        except KeyboardInterrupt:
            print("\n\n⚠️  Scan stopped by user!\n")
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
