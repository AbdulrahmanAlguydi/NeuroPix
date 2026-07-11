import os
import time
import sys
from services.image_service import save_image_transaction
from database.queries import register_user, get_user_by_username, get_user_gallery

def run_integrated_workflow():
    print("==================================================")
    print("STARTING INTEGRATED S3 KEY AND DATABASE WORKFLOW")
    print("==================================================")

    local_raw_path = "user_upload_raw.jpg"
    local_edited_path = "system_output_ai.jpg"

    with open(local_raw_path, "w") as f:
        f.write("simulated raw binary image payload data")
    with open(local_edited_path, "w") as f:
        f.write("simulated ai modified binary image payload data")

    try:
        unique_suffix = int(time.time())
        username = f"workflow_user_{unique_suffix}"
        password_hash = "hashed_workflow_password_123"

        print(f"[STEP 1] Registering temporary workflow user: {username}")
        if not register_user(username, password_hash):
            print("[ERROR] Failed to register workflow user.")
            sys.exit(1)

        user = get_user_by_username(username)
        user_id = user["UserID"]
        print(f"[OK] User resolved with database UserID: {user_id}")

        print("\n[STEP 2] Executing Single-Step Image Pipeline Transaction...")
        result = save_image_transaction(
            user_id=user_id,
            local_raw_path=local_raw_path,
            local_edited_path=local_edited_path,
            edit_type="ai"
        )

        if not result:
            print("[ERROR] Integrated image transaction pipeline failed.")
            sys.exit(1)

        print("\n[STEP 3] Verifying database records via user gallery retrieval...")
        gallery = get_user_gallery(user_id)
        if gallery:
            print("\n🎉 [SUCCESS] Integrated pipeline run completed clean.")
            print(f"Verified logged database row data: {gallery[0]}")
        else:
            print("[ERROR] Verification failed: Logged item not returned in gallery query.")
            sys.exit(1)

    finally:
        print("\nCleaning up local temporary mock files...")
        for file_path in [local_raw_path, local_edited_path]:
            if os.path.exists(file_path):
                os.remove(file_path)

    print("==================================================")

if __name__ == "__main__":
    run_integrated_workflow()