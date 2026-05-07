# ============================================
# Password Strength Checker
# Built by: [Your Name]
# Project: Cybersecurity Side Project #1
# ============================================

import re  # re = regular expressions, used for pattern matching

# ---- COMMON PASSWORDS LIST ----
# These are passwords hackers try FIRST
COMMON_PASSWORDS = [
    "password", "123456", "password1", "12345678", "qwerty",
    "abc123", "monkey", "letmein", "trustno1", "dragon",
    "iloveyou", "master", "sunshine", "shadow", "123123",
    "superman", "michael", "football", "admin", "welcome",
    "login", "pass", "test", "1234", "111111", "root",
    "pass123", "changeme", "hello", "password123"
]


# ---- CHECK FUNCTIONS ----
# Each function checks ONE thing about the password

def check_length(password):
    """Check if password is long enough"""
    if len(password) >= 12:
        return True, "✓ Length is strong (12+ characters)"
    elif len(password) >= 8:
        return True, "~ Length is okay (8+ characters) — try 12+"
    else:
        return False, "✗ Too short — use at least 8 characters"


def check_uppercase(password):
    """Check if password has uppercase letters"""
    if re.search(r'[A-Z]', password):
        return True, "✓ Has uppercase letters"
    else:
        return False, "✗ Missing uppercase letters (A-Z)"


def check_lowercase(password):
    """Check if password has lowercase letters"""
    if re.search(r'[a-z]', password):
        return True, "✓ Has lowercase letters"
    else:
        return False, "✗ Missing lowercase letters (a-z)"


def check_numbers(password):
    """Check if password has numbers"""
    if re.search(r'[0-9]', password):
        return True, "✓ Has numbers"
    else:
        return False, "✗ Missing numbers (0-9)"


def check_special_chars(password):
    """Check if password has special characters"""
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return True, "✓ Has special characters (!@#$...)"
    else:
        return False, "✗ Missing special characters (!@#$%^&*)"


def check_common(password):
    """Check if password is a commonly used password"""
    if password.lower() in COMMON_PASSWORDS:
        return False, "✗ This is a COMMON password — hackers will crack it instantly!"
    else:
        return True, "✓ Not a common password"


def check_repeated_chars(password):
    """Check for repeated characters like 'aaa' or '111'"""
    if re.search(r'(.)\1{2,}', password):
        return False, "✗ Has repeated characters (e.g. aaa, 111) — avoid this"
    else:
        return True, "✓ No repeated characters"


# ---- CALCULATE SCORE ----
def calculate_score(results):
    """Give a score out of 100 based on checks passed"""
    score = 0
    # Each check adds points
    points = [20, 15, 10, 15, 20, 10, 10]  # points per check
    for i, (passed, _) in enumerate(results):
        if passed:
            score += points[i]
    return min(score, 100)  # max is 100


# ---- GET STRENGTH LABEL ----
def get_strength(score, common_check_passed):
    """Return a label based on the score"""
    if not common_check_passed:
        return "💀 CRITICALLY WEAK"
    elif score < 30:
        return "🔴 VERY WEAK"
    elif score < 50:
        return "🟠 WEAK"
    elif score < 70:
        return "🟡 MODERATE"
    elif score < 90:
        return "🟢 STRONG"
    else:
        return "🔵 VERY STRONG"


# ---- ESTIMATE CRACK TIME ----
def estimate_crack_time(password):
    """Roughly estimate how long it takes to crack"""
    charset = 0
    if re.search(r'[a-z]', password): charset += 26
    if re.search(r'[A-Z]', password): charset += 26
    if re.search(r'[0-9]', password): charset += 10
    if re.search(r'[^A-Za-z0-9]', password): charset += 32

    if charset == 0:
        return "Instantly"

    combinations = charset ** len(password)
    guesses_per_second = 10_000_000_000  # 10 billion (modern GPU)
    seconds = combinations / guesses_per_second

    if seconds < 1:
        return "Instantly"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds // 60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} hours"
    elif seconds < 2592000:
        return f"{int(seconds // 86400)} days"
    elif seconds < 31536000:
        return f"{int(seconds // 2592000)} months"
    else:
        return f"{int(seconds // 31536000):,} years"


# ---- MAIN FUNCTION ----
def check_password(password):
    """Run all checks and display results"""

    print("\n" + "=" * 50)
    print("   PASSWORD STRENGTH ANALYZER")
    print("=" * 50)
    print(f"   Analyzing: {'*' * len(password)}")
    print(f"   Length: {len(password)} characters")
    print("=" * 50)

    # Run all checks
    results = [
        check_length(password),
        check_uppercase(password),
        check_lowercase(password),
        check_numbers(password),
        check_special_chars(password),
        check_common(password),
        check_repeated_chars(password),
    ]

    # Print each check result
    print("\n📋 SECURITY CHECKS:")
    print("-" * 40)
    for passed, message in results:
        print(f"   {message}")

    # Calculate and show score
    score = calculate_score(results)
    common_passed = results[5][0]  # index 5 is the common password check
    strength = get_strength(score, common_passed)
    crack_time = estimate_crack_time(password)

    print("\n" + "-" * 40)
    print(f"   SCORE:      {score}/100")
    print(f"   STRENGTH:   {strength}")
    print(f"   CRACK TIME: {crack_time}")
    print("=" * 50)

    # Give advice
    print("\n💡 ADVICE:")
    failed = [msg for passed, msg in results if not passed]
    if not failed:
        print("   Excellent! Your password passed all checks.")
    else:
        print("   Fix these issues to improve your password:")
        for msg in failed:
            print(f"   → {msg.replace('✗ ', '')}")

    print("=" * 50 + "\n")


# ---- RUN THE PROGRAM ----
if __name__ == "__main__":
    print("\n🔐 Welcome to Password Strength Checker")
    print("   Type 'quit' to exit\n")

    while True:
        password = input("Enter a password to check: ")

        if password.lower() == 'quit':
            print("\n👋 Goodbye!\n")
            break

        if not password:
            print("⚠️  Please enter a password!\n")
            continue

        check_password(password)
