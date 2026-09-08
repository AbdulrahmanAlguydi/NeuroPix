import sys
import uuid
from pathlib import Path

# Add the project root so this file can be run directly from VS Code.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from database.database import get_db_connection
from database.queries import (
    get_user_by_username,
    get_user_gallery,
    log_image_edit,
    register_user,
)


def cleanup_test_data(user_id):
    """Remove the temporary user and image row created by this check."""
    if not user_id:
        return

    connection = get_db_connection()
    if not connection:
        print("[WARNING] Could not connect for database cleanup.")
        return

    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Images WHERE UserID = %s;", (user_id,))
        cursor.execute("DELETE FROM Users WHERE UserID = %s;", (user_id,))
        connection.commit()
        print("[CLEANUP] Removed temporary database records.")
    except Exception as error:
        connection.rollback()
        print(f"[WARNING] Database cleanup failed: {error}")
    finally:
        cursor.close()
        connection.close()


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
        if connection and connection.is_connected():
            print(
                "  [SUCCESS] Successfully established a network connection to the database server."
            )
            connection.close()
        else:
            print("  [FAILED] Connection object is inactive or server is offline.")
            sys.exit(1)
    except Exception as err:
        print(f"  [ERROR] Network handshake failed: {err}")
        sys.exit(1)

    # ---------------------------------------------------------------------
    # STAGE 2: Functional Repository Integration Tests
    # ---------------------------------------------------------------------
    print("\n[STAGE 2/2] Running Schema-Validated Integration Tests...")

    target_user_id = None
    try:
        unique_suffix = uuid.uuid4().hex[:8]
        test_username = f"integration_user_{unique_suffix}"
        test_password_hash = "secure_hashed_string_999"
        fake_orig_path = f"inputs/integration-{unique_suffix}-raw.jpg"
        fake_mod_path = f"outputs/integration-{unique_suffix}-edited.jpg"

        # 1. Test registration
        print("\n  [TEST 1/4] Running register_user()...")
        if register_user(test_username, test_password_hash):
            print("    [SUCCESS] Inserted test record into 'Users' table.")
        else:
            print("    [FAILED] Could not insert the test user.")
            sys.exit(1)

        # 2. Test user lookup
        print("\n  [TEST 2/4] Running get_user_by_username()...")
        fetched_user = get_user_by_username(test_username)
        if fetched_user and fetched_user["Username"] == test_username:
            print("    [SUCCESS] Selected row from 'Users'.")
            print(f"    Captured Data: {fetched_user}")
            target_user_id = fetched_user["UserID"]
        else:
            print("    [FAILED] Could not resolve the test user.")
            sys.exit(1)

        # 3. Test image write integration
        print("\n  [TEST 3/4] Running log_image_edit()...")
        if log_image_edit(target_user_id, fake_orig_path, fake_mod_path, "ai"):
            print("    [SUCCESS] Inserted a linked image record.")
        else:
            print("    [FAILED] Could not insert the image record.")
            sys.exit(1)

        # 4. Test gallery stream mapping
        print("\n  [TEST 4/4] Running get_user_gallery()...")
        user_gallery = get_user_gallery(target_user_id)
        if user_gallery and user_gallery[0]["ModifiedFilePath"] == fake_mod_path:
            print("    [SUCCESS] Retrieved the image record from the gallery query.")
            print(f"    Captured Gallery Record: {user_gallery[0]}")
        else:
            print("    [FAILED] Gallery lookup returned the wrong data.")
            sys.exit(1)

        print("\n==================================================")
        print("ALL DATABASE AND INTEGRATION TESTS PASSED SUCCESSFULLY")
        print("==================================================")
    finally:
        cleanup_test_data(target_user_id)


if __name__ == "__main__":
    run_tests()
