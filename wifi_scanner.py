# ============================================
# WiFi Security Scanner
# Built by: Kainat
# Project 5 — Cybersecurity Portfolio
# Helps people check if public WiFi is safe!
# ============================================

import socket
import datetime
import subprocess
import platform

# ---- SUSPICIOUS WIFI NAMES ----
SUSPICIOUS_NAMES = [
    "free wifi", "freewifi", "free_wifi", "free-wifi",
    "public wifi", "publicwifi", "public_wifi",
    "airport wifi", "airport_wifi", "airportwifi",
    "hotel wifi", "hotel_wifi", "hotelwifi",
    "coffee wifi", "coffeewifi", "starbucks",
    "mcdonalds", "mall wifi", "mall_wifi",
    "guest wifi", "guestwifi", "guest_wifi",
    "open wifi", "openwifi", "open_wifi",
    "hack", "hacker", "evil twin", "eviltwin",
    "interceptor", "spy", "monitor", "sniff",
    "linksys", "netgear", "dlink", "default",
    "admin", "password", "test", "router"
]

# ---- SAFE ENCRYPTION TYPES ----
ENCRYPTION_SAFETY = {
    "wpa3":   ("🟢 VERY SECURE", "WPA3 is the latest and strongest encryption!"),
    "wpa2":   ("🟢 SECURE", "WPA2 is good encryption — standard for most networks"),
    "wpa":    ("🟡 MODERATE", "WPA is older — consider asking for WPA2/WPA3"),
    "wep":    ("🔴 DANGEROUS", "WEP is broken! Hackers can crack it in minutes!"),
    "open":   ("🔴 VERY DANGEROUS", "No encryption! Anyone can see your data!"),
    "none":   ("🔴 VERY DANGEROUS", "No encryption! Anyone can see your data!"),
    "unknown":("🟡 UNKNOWN", "Cannot determine encryption — be careful!")
}

# ---- CHECK WIFI NAME ----
def check_wifi_name(name):
    """Check if WiFi name looks suspicious"""
    name_lower = name.lower().strip()

    # Check against suspicious names
    for suspicious in SUSPICIOUS_NAMES:
        if suspicious in name_lower:
            return True, f"Name '{name}' matches suspicious pattern '{suspicious}'"

    # Check for all numbers (like "12345678")
    if name.replace(" ", "").isdigit():
        return True, "WiFi name is all numbers — suspicious!"

    # Check for very short names
    if len(name) <= 2:
        return True, "WiFi name is too short — suspicious!"

    return False, f"Name '{name}' looks normal"

# ---- GET WINDOWS WIFI INFO ----
def get_windows_wifi():
    """Get current WiFi info on Windows/WSL"""
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            capture_output=True, text=True, shell=True
        )
        return result.stdout
    except:
        return None

# ---- SCAN WIFI MANUALLY ----
def manual_wifi_scan(ssid, encryption, signal):
    """Analyze WiFi based on user input"""

    print("\n" + "=" * 60)
    print("   📡 WIFI SECURITY SCANNER — by Kainat")
    print("=" * 60)
    print(f"   Network Name : {ssid}")
    print(f"   Encryption   : {encryption.upper()}")
    print(f"   Signal       : {signal}%")
    print(f"   Scanned at   : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    risk_score = 0
    warnings = []
    advice = []

    # Check 1 — WiFi name
    print("\n🔍 RUNNING SECURITY CHECKS...\n")
    is_suspicious, name_reason = check_wifi_name(ssid)
    if is_suspicious:
        risk_score += 30
        warnings.append(f"⚠️  Suspicious name: {name_reason}")
        advice.append("Verify this is the official network with staff")
    else:
        print(f"   ✅ Network name looks legitimate")

    # Check 2 — Encryption
    enc_lower = encryption.lower().strip()
    if enc_lower in ENCRYPTION_SAFETY:
        status, message = ENCRYPTION_SAFETY[enc_lower]
        print(f"   {status} Encryption: {message}")
        if "DANGEROUS" in status:
            risk_score += 40
            warnings.append(f"🔴 Weak encryption: {message}")
            advice.append("Avoid entering passwords on this network!")
            advice.append("Use a VPN if you must connect!")
        elif "MODERATE" in status:
            risk_score += 15
            warnings.append(f"🟡 Older encryption: {message}")
    else:
        risk_score += 20
        warnings.append("Unknown encryption type detected")

    # Check 3 — Signal strength
    signal_int = int(signal)
    if signal_int > 90:
        risk_score += 15
        warnings.append("⚠️  Unusually strong signal — possible fake hotspot nearby!")
        advice.append("Very strong unknown signals can indicate evil twin attacks")
        print(f"   ⚠️  Signal too strong ({signal}%) — suspicious!")
    elif signal_int > 60:
        print(f"   ✅ Signal strength normal ({signal}%)")
    else:
        print(f"   ✅ Signal strength low-medium ({signal}%) — normal")

    # Check 4 — Open network
    if enc_lower in ["open", "none", ""]:
        risk_score += 30
        warnings.append("🔴 OPEN NETWORK — No password required = no protection!")
        advice.append("NEVER do banking or enter passwords on open networks!")
        advice.append("Use mobile data instead if possible!")

    # ---- FINAL VERDICT ----
    print("\n" + "=" * 60)
    print("   SECURITY ANALYSIS RESULTS")
    print("=" * 60)

    if warnings:
        print("\n⚠️  WARNINGS FOUND:")
        for w in warnings:
            print(f"   {w}")

    # Determine verdict
    print("\n" + "-" * 40)
    if risk_score >= 60:
        verdict = "🔴 DANGEROUS — DO NOT USE!"
        verdict_detail = "This network has serious security issues!"
    elif risk_score >= 30:
        verdict = "🟡 SUSPICIOUS — USE WITH CAUTION!"
        verdict_detail = "This network has some security concerns"
    elif risk_score >= 10:
        verdict = "🟡 MODERATE — BE CAREFUL"
        verdict_detail = "This network is okay but take precautions"
    else:
        verdict = "🟢 LOOKS SAFE"
        verdict_detail = "This network appears to be secure"

    print(f"\n   VERDICT: {verdict}")
    print(f"   {verdict_detail}")
    print(f"   Risk Score: {min(risk_score, 100)}/100")

    # Safety advice
    print("\n💡 SAFETY ADVICE:")
    print("-" * 40)

    # Always show these tips
    default_advice = [
        "Always use HTTPS websites (look for 🔒 in browser)",
        "Use a VPN for extra protection on public WiFi",
        "Never do online banking on public WiFi",
        "Turn off file sharing when on public networks",
        "Forget the network when done using it"
    ]

    for tip in (advice + default_advice):
        print(f"   → {tip}")

    print("=" * 60 + "\n")

# ---- RUN THE PROGRAM ----
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("   📡 WIFI SECURITY SCANNER by Kainat")
    print("   Helps you stay safe on public WiFi!")
    print("=" * 60)

    print("\n📋 Enter your WiFi details:\n")

    # Get WiFi name
    ssid = input("WiFi Name (SSID): ").strip()
    if not ssid:
        ssid = "Unknown Network"

    # Get encryption type
    print("\nEncryption types: WPA3 / WPA2 / WPA / WEP / Open")
    encryption = input("Encryption Type: ").strip()
    if not encryption:
        encryption = "unknown"

    # Get signal strength
    print("\nSignal strength (0-100%)")
    signal = input("Signal Strength %: ").strip()
    if not signal or not signal.isdigit():
        signal = "50"
    signal = str(min(max(int(signal), 0), 100))

    # Run scan
    try:
        manual_wifi_scan(ssid, encryption, signal)
    except KeyboardInterrupt:
        print("\n\n⚠️  Scan stopped by user!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
