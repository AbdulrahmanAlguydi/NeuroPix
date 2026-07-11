import os
import uuid
from pathlib import Path
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

# Initialize the S3 client resource
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def _execute_s3_upload(local_file_path, folder_prefix):
    """
    Internal helper function to handle core S3 configuration, unique filename 
    generation, and stream transmission to AWS.
    """
    path = Path(local_file_path)
    if not path.exists():
        print(f"  [ERROR] Local file not found at path: {local_file_path}")
        return None

    # Generate a unique filename while preserving the original file extension
    file_extension = path.suffix.lower()
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    s3_object_key = f"{folder_prefix}/{unique_filename}"

    try:
        print(f"  Uploading {path.name} to storage bucket path: '{AWS_BUCKET_NAME}'...")
        
        s3_client.upload_file(
            Filename=str(path),
            Bucket=AWS_BUCKET_NAME,
            Key=s3_object_key,
            ExtraArgs={"ContentType": f"image/{file_extension.strip('.')}"}
        )
        
        # Build public access URL
        s3_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_object_key}"
        return s3_url

    except NoCredentialsError:
        print("  [ERROR] AWS credentials missing. Verify your .env setup.")
        return None
    except ClientError as err:
        print(f"  [ERROR] AWS S3 gateway error: {err}")
        return None
    except Exception as err:
        print(f"  [ERROR] Unexpected error during transport sequence: {err}")
        return None


# =========================================================================
# PUBLIC REUSABLE STORAGE UTILITIES
# =========================================================================

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


# =========================================================================
# ISOLATED UNIT TEST RUNNER
# =========================================================================
# if __name__ == "__main__":
#     print("==================================================")
#     print("STARTING DUAL-PATH AWS S3 STORAGE TESTS")
#     print("==================================================")
    
#     # Create distinct local temporary mock assets
#     input_mock = "temp_raw_upload.jpg"
#     output_mock = "temp_processed_output.jpg"
    
#     with open(input_mock, "w") as f:
#         f.write("raw pixel image simulation stream")
#     with open(output_mock, "w") as f:
#         f.write("processed pixel image simulation stream")

#     # 1. Test Original Path Upload
#     print("\n[TEST 1/2] Validating upload_original_image()...")
#     input_url = upload_original_image(input_mock)
#     if input_url and "/inputs/" in input_url:
#         print(f"  [SUCCESS] Raw asset hit target node. URL: {input_url}")
#     else:
#         print("  [FAILED] Raw file upload routing failed.")

#     # 2. Test Processed Path Upload
#     print("\n[TEST 2/2] Validating upload_processed_image()...")
#     output_url = upload_processed_image(output_mock)
#     if output_url and "/outputs/" in output_url:
#         print(f"  [SUCCESS] Edited asset hit target node. URL: {output_url}")
#     else:
#         print("  [FAILED] Edited file upload routing failed.")

#     # Clean up local mock workspace environment
#     for mock_file in [input_mock, output_mock]:
#         if os.path.exists(mock_file):
#             os.remove(mock_file)

#     print("\n==================================================")
#     print("S3 STORAGE ROUTING VALIDATION TEST CYCLE COMPLETE")
#     print("==================================================")