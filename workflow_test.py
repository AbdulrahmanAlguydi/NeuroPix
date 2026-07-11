import os
import time
import sys
from utils.s3 import upload_original_image, upload_processed_image
from database.queries import register_user, get_user_by_username, log_image_edit, get_user_gallery

def run_integrated_workflow():
    print("==================================================")
    print("STARTING INTEGRATED S3 UPLOAD AND DATABASE WORKFLOW")
    print("==================================================")

    # Create mock local files to simulate images waiting on the server
    local_raw_path = "user_upload_raw.jpg"
    local_edited_path = "system_output_ai.jpg"

    with open(local_raw_path, "w") as f:
        f.write("simulated raw binary image payload data")
    with open(local_edited_path, "w") as f:
        f.write("simulated ai modified binary image payload data")

    try:
        # Step 1: Ensure a valid user exists to assign the images to
        unique_suffix = int(time.time())
        username = f"workflow_user_{unique_suffix}"
        password_hash = "hashed_workflow_password_123"

        print(f"[STEP 1] Registering temporary workflow user: {username}")
        if not register_user(username, password_hash):
            print("[ERROR] Failed to register workflow user.")
            sys.exit(1)

        user = get_user_by_username(username)
        if not user:
            print("[ERROR] Failed to retrieve newly registered user.")
            sys.exit(1)

        user_id = user["UserID"]
        print(f"[OK] User resolved with database UserID: {user_id}")

        # Step 2: Upload the original raw image to S3 (inputs folder)
        print("\n[STEP 2] Uploading original file to AWS S3 storage...")
        original_s3_url = upload_original_image(local_raw_path)
        if not original_s3_url:
            print("[ERROR] S3 raw upload failed.")
            sys.exit(1)
        print(f"[OK] Original S3 URL generated: {original_s3_url}")

        # Step 3: Upload the processed AI image to S3 (outputs folder)
        print("\n[STEP 3] Uploading processed file to AWS S3 storage...")
        modified_s3_url = upload_processed_image(local_edited_path)
        if not modified_s3_url:
            print("[ERROR] S3 processed upload failed.")
            sys.exit(1)
        print(f"[OK] Modified S3 URL generated: {modified_s3_url}")

        # Step 4: Log the entire transaction records into the MySQL Images table
        print("\n[STEP 4] Recording S3 storage paths into the database...")
        edit_type = "ai"  # Must match your database schema ENUM ('standard', 'ai')
        db_success = log_image_edit(
            user_id=user_id,
            original_path=original_s3_url,
            modified_path=modified_s3_url,
            edit_type=edit_type
        )

        if db_success:
            print("[OK] Transaction row inserted into 'Images' table successfully.")
        else:
            print("[ERROR] Database logging operation failed.")
            sys.exit(1)

        # Step 5: Verify the workflow record can be pulled via the user's gallery stream
        print("\n[STEP 5] Verifying database records via user gallery retrieval...")
        gallery = get_user_gallery(user_id)
        if gallery:
            print("\n[SUCCESS] Integrated pipeline run completed clean.")
            print(f"Verified logged database row data: {gallery[0]}")
        else:
            print("[ERROR] Verification failed: Logged item not returned in gallery query.")
            sys.exit(1)

    finally:
        # Clean up local workspace environment files
        print("\nCleaning up local temporary mock files...")
        for file_path in [local_raw_path, local_edited_path]:
            if os.path.exists(file_path):
                os.remove(file_path)

    print("==================================================")
    print("INTEGRATED WORKFLOW EXECUTION COMPLETED SUCCESSFULLY")
    print("==================================================")

if __name__ == "__main__":
    run_integrated_workflow()