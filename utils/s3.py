import os

import boto3
from dotenv import load_dotenv

load_dotenv()

# Create one S3 client using credentials supplied by the local environment.
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=AWS_REGION,
)


def _execute_s3_upload(local_file_path, folder_prefix):
    """Upload a local image and return its S3 object key."""
    if not os.path.exists(local_file_path):
        print(f"[STORAGE ERROR] Local file not found: {local_file_path}")
        return None

    filename = os.path.basename(local_file_path)

    # Keep originals and processed files in separate folders in the bucket.
    object_key = f"{folder_prefix}/{filename}"

    try:
        # S3 needs the correct type so browsers can display the returned image.
        content_type = "image/png"
        if filename.lower().endswith((".jpg", ".jpeg")):
            content_type = "image/jpeg"

        s3_client.upload_file(
            Filename=local_file_path,
            Bucket=AWS_BUCKET_NAME,
            Key=object_key,
            ExtraArgs={"ContentType": content_type},
        )
        print(f"[STORAGE] Upload complete. Object key registered: {object_key}")
        return object_key

    except Exception as err:
        print(f"[STORAGE ERROR] Upload failed: {err}")
        return None


def upload_original_image(local_file_path):
    """Upload an original image to the inputs folder."""
    return _execute_s3_upload(local_file_path, folder_prefix="inputs")


def upload_processed_image(local_file_path):
    """Upload a processed image to the outputs folder."""
    return _execute_s3_upload(local_file_path, folder_prefix="outputs")


def get_full_s3_url(object_key):
    """Convert an S3 object key into a public URL."""
    if not object_key:
        return None
    return f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{object_key}"


def download_s3_object(object_key, local_file_path):
    """Download one S3 object to a local path."""
    if not object_key:
        return False

    try:
        s3_client.download_file(
            Bucket=AWS_BUCKET_NAME,
            Key=object_key,
            Filename=local_file_path,
        )
        return True
    except Exception as err:
        print(f"[STORAGE ERROR] Download failed: {err}")
        return False


def delete_s3_object(object_key):
    """Delete one object from S3."""
    if not object_key:
        return True  # Nothing to delete

    try:
        s3_client.delete_object(Bucket=AWS_BUCKET_NAME, Key=object_key)
        print(f"[STORAGE] Successfully deleted from S3: {object_key}")
        return True
    except Exception as err:
        print(f"[STORAGE ERROR] Failed to delete {object_key}: {err}")
        return False
