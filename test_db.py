import time
import sys
from database.database import get_db_connection
from database.queries import register_user, get_user_by_username, log_image_edit, get_user_gallery

def run_tests():
    print("==================================================")
    print("STARTING COMPLETE DATABASE VALIDATION TEST SUITE")
    print("==================================================")

    # ---------------------------------------------------------------------
    # STAGE 1: Network Connection Test
    # ---------------------------------------------------------------------
    print("\n[STAGE 1/2] Testing Core Database Connection...")
    try:
        connection = get_db_connection()
        if connection.is_connected():
            print("  [SUCCESS] Successfully established a network connection to the database server.")
            connection.close()
        else:
            print("  [FAILED] Connection object created but reporting inactive status.")
            sys.exit(1)
    except Exception as err:
        print(f"  [ERROR] Network handshake failed: {err}")
        sys.exit(1)

    # ---------------------------------------------------------------------
    # STAGE 2: Functional Repository Integration Tests
    # ---------------------------------------------------------------------
    print("\n[STAGE 2/2] Running Schema-Validated Integration Tests...")
    
    unique_suffix = int(time.time())
    test_username = f"user_{unique_suffix}"
    test_password_hash = "secure_hashed_string_999"
    
    fake_orig_path = f"https://neuropix-storage.s3.amazonaws.com/inputs/{unique_suffix}_raw.jpg"
    fake_mod_path = f"https://neuropix-storage.s3.amazonaws.com/outputs/{unique_suffix}_edited.jpg"
    fake_edit_type = "ai"

    # 1. Test registration
    print("\n  [TEST 1/4] Running register_user()...")
    if register_user(test_username, test_password_hash):
        print(f"    [SUCCESS] Inserted test record into 'Users' table.")
    else:
        print("    [FAILED] Registration query failed syntax or constraint verification.")
        sys.exit(1)

    # 2. Test user lookup
    print("\n  [TEST 2/4] Running get_user_by_username()...")
    fetched_user = get_user_by_username(test_username)
    if fetched_user and fetched_user['Username'] == test_username:
        print(f"    [SUCCESS] Selected row from 'Users'.")
        print(f"    Captured Data: {fetched_user}")
        target_user_id = fetched_user['UserID']
    else:
        print("    [FAILED] Could not resolve Username or columns mismatched.")
        sys.exit(1)

    # 3. Test image write integration
    print("\n  [TEST 3/4] Running log_image_edit()...")
    if log_image_edit(target_user_id, fake_orig_path, fake_mod_path, fake_edit_type):
        print(f"    [SUCCESS] Inserted image transaction into 'Images' table via foreign key link.")
    else:
        print("    [FAILED] Image insertion failed. Check column names or ENUM constraints.")
        sys.exit(1)

    # 4. Test gallery stream mapping
    print("\n  [TEST 4/4] Running get_user_gallery()...")
    user_gallery = get_user_gallery(target_user_id)
    if len(user_gallery) > 0 and user_gallery[0]['ModifiedFilePath'] == fake_mod_path:
        print(f"    [SUCCESS] Selected historical stack from 'Images'.")
        print(f"    Captured Gallery Record: {user_gallery[0]}")
    else:
        print("    [FAILED] Gallery lookup came back empty or keys broke.")
        sys.exit(1)

    print("\n==================================================")
    print("ALL DATABASE AND INTEGRATION TESTS PASSED SUCCESSFULLY")
    print("==================================================")

if __name__ == "__main__":
    run_tests()