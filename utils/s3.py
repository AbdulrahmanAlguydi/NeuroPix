import os
import uuid  # Added for generating unique object keys
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=AWS_REGION
)

def _execute_s3_upload(local_file_path, folder_prefix):
    """
    Core private handler that uploads a local file to S3 
    and returns its unique, collision-safe object key location.
    """
    if not os.path.exists(local_file_path):
        print(f"[STORAGE ERROR] Local file not found: {local_file_path}")
        return None

    filename = os.path.basename(local_file_path)
    
    # Generate a unique 8-character token (e.g., 'a1c2e3f4')
    unique_suffix = uuid.uuid4().hex[:8]
    
    # Prepend the token to the filename to guarantee uniqueness in S3
    object_key = f"{folder_prefix}/{unique_suffix}_{filename}"

    try:
        content_type = "image/jpeg" if filename.lower().endswith(('.jpg', '.jpeg')) else "image/png"

        s3_client.upload_file(
            Filename=local_file_path,
            Bucket=AWS_BUCKET_NAME,
            Key=object_key,
            ExtraArgs={"ContentType": content_type}
        )
        print(f"[STORAGE] Upload complete. Unique key registered: {object_key}")
        return object_key  # Returns e.g., 'inputs/a1c2e3f4_avatar.png'

    except Exception as err:
        print(f"[STORAGE ERROR] Upload failed: {err}")
        return None


def upload_original_image(local_file_path):
    """
    Uploads a raw user-uploaded file into the 'inputs' folder prefix.
    Maps to OriginalFilePath in the database schema.
    """
    print("[STORAGE] Initializing raw image upload sequence...")
    return _execute_s3_upload(local_file_path, folder_prefix="inputs")


def upload_processed_image(local_file_path):
    """
    Uploads an already edited file into the 'outputs' folder prefix.
    Maps to ModifiedFilePath in the database schema.
    """
    print("[STORAGE] Initializing processed image upload sequence...")
    return _execute_s3_upload(local_file_path, folder_prefix="outputs")