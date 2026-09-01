import sys
from pathlib import Path

# Add the project root so this file can be run directly from VS Code.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.security import hash_password, verify_password

def run_tests():
    print("==================================================")
    print("STARTING PASSWORD HASHING VALIDATION TEST")
    print("==================================================")

    plain_password = "correct_horse_battery_staple"
    wrong_password = "wrong_password_123"

    # 1. Test hashing
    print("\n[TEST 1/3] Hashing a password...")
    password_hash = hash_password(plain_password)
    if password_hash and password_hash != plain_password:
        print(f"  [SUCCESS] Password hashed. Hash starts with: {password_hash[:30]}...")
    else:
        print("  [FAILED] Password was not hashed correctly.")
        sys.exit(1)

    # 2. Test correct password verification
    print("\n[TEST 2/3] Verifying the correct password...")
    if verify_password(plain_password, password_hash):
        print("  [SUCCESS] Correct password verified successfully.")
    else:
        print("  [FAILED] Correct password did not verify.")
        sys.exit(1)

    # 3. Test incorrect password verification
    print("\n[TEST 3/3] Verifying an incorrect password...")
    if not verify_password(wrong_password, password_hash):
        print("  [SUCCESS] Incorrect password was correctly rejected.")
    else:
        print("  [FAILED] Incorrect password was accepted!")
        sys.exit(1)

    print("\n==================================================")
    print("ALL PASSWORD HASHING TESTS PASSED SUCCESSFULLY")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
