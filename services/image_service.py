from utils.s3 import upload_original_image, upload_processed_image
from database.queries import log_image_edit

def save_image_transaction(user_id, local_raw_path, local_edited_path=None, edit_type=None):
    """
    Handles the complete image storage lifecycle for NeuroPix.
    1. Uploads the raw image to the S3 'inputs' directory.
    2. Uploads the processed image to the S3 'outputs' directory (if provided).
    3. Commits the resulting cloud storage URLs to the MySQL database Images table.

    Args:
        user_id (int): The primary key ID of the user owning the asset.
        local_raw_path (str): File system path to the original uploaded image.
        local_edited_path (str, optional): File system path to the processed output.
        edit_type (str, optional): The type of modification applied ('standard' or 'ai').

    Returns:
        dict: A dictionary containing the logged file paths if successful, None otherwise.
    """
    print(f"[SERVICE] Starting integrated image storage pipeline for UserID: {user_id}")

    # 1. Transport the original image to S3 inputs folder and get its object key
    original_s3_key = upload_original_image(local_raw_path)
    if not original_s3_key:
        print("[SERVICE ERROR] Pipeline aborted: S3 raw file transmission failed.")
        return None

    # 2. Transport the processed image to S3 outputs folder and get its object key (if one exists)
    modified_s3_key = None
    if local_edited_path:
        modified_s3_key = upload_processed_image(local_edited_path)
        if not modified_s3_key:
            print("[SERVICE ERROR] Pipeline aborted: S3 processed file transmission failed.")
            return None

    # 3. Write transaction metadata records to the MySQL Database
    db_success = log_image_edit(
        user_id=user_id,
        original_path=original_s3_key,
        modified_path=modified_s3_key,
        edit_type=edit_type
    )

    if not db_success:
        print("[SERVICE ERROR] Pipeline failed: Files uploaded to S3, but database registration failed.")
        return None

    print("[SERVICE SUCCESS] Image pipeline completed cleanly. Data committed to S3 and DB.")
    
    # Return structured tracking details to the caller
    return {
        "OriginalFilePath": original_s3_key,
        "ModifiedFilePath": modified_s3_key,
        "EditType": edit_type
    }