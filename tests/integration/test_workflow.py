import os
import sys
import uuid
from pathlib import Path
from tempfile import TemporaryDirectory

# Add the project root so this file can be run directly.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from database.database import get_db_connection
from database.queries import get_user_by_username, get_user_gallery, register_user
from services.image_service import save_image_transaction
from utils.s3 import delete_s3_object


def cleanup_database_user(user_id):
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


def run_integrated_workflow():
    print("==================================================")
    print("STARTING INTEGRATED S3 KEY AND DATABASE WORKFLOW")
    print("==================================================")

    user_id = None
    result = None
    unique_suffix = uuid.uuid4().hex[:8]

    with TemporaryDirectory(prefix="neuropix-integration-") as temp_dir:
        local_raw_path = os.path.join(temp_dir, f"integration-{unique_suffix}-raw.jpg")
        local_edited_path = os.path.join(
            temp_dir, f"integration-{unique_suffix}-edited.jpg"
        )

        with open(local_raw_path, "w") as raw_file:
            raw_file.write("simulated raw binary image payload data")
        with open(local_edited_path, "w") as edited_file:
            edited_file.write("simulated ai modified binary image payload data")

        try:
            username = f"workflow_user_{unique_suffix}"
            password_hash = "hashed_workflow_password_123"

            print(f"[STEP 1] Registering temporary workflow user: {username}")
            if not register_user(username, password_hash):
                print("[ERROR] Failed to register workflow user.")
                sys.exit(1)

            user = get_user_by_username(username)
            if not user:
                print("[ERROR] Could not resolve the workflow user.")
                sys.exit(1)
            user_id = user["UserID"]
            print(f"[OK] User resolved with database UserID: {user_id}")

            print("\n[STEP 2] Executing Single-Step Image Pipeline Transaction...")
            result = save_image_transaction(
                user_id=user_id,
                local_raw_path=local_raw_path,
                local_edited_path=local_edited_path,
                edit_type="ai",
            )

            if not result:
                print("[ERROR] Integrated image transaction pipeline failed.")
                sys.exit(1)

            print("\n[STEP 3] Verifying database records via user gallery retrieval...")
            gallery = get_user_gallery(user_id)
            if gallery:
                print("\n[SUCCESS] Integrated pipeline run completed clean.")
                print(f"Verified logged database row data: {gallery[0]}")
            else:
                print(
                    "[ERROR] Verification failed: Logged item not returned in gallery query."
                )
                sys.exit(1)
        finally:
            if result:
                delete_s3_object(result.get("OriginalFilePath"))
                delete_s3_object(result.get("ModifiedFilePath"))
            cleanup_database_user(user_id)
            print("\n[CLEANUP] Removed temporary workflow files and records.")

    print("==================================================")


if __name__ == "__main__":
    run_integrated_workflow()
