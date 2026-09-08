import os
import sys
import uuid

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv


def run_tests():
    # Load environment variables from .env
    load_dotenv()

    print("=========================================")
    print("NEUROPIX: Testing AWS S3 Storage...")
    print("=========================================")

    # Retrieve keys from environment
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    region_name = os.getenv("AWS_REGION")

    s3 = None
    test_file_key = f"integration-tests/s3-test-{uuid.uuid4().hex}.txt"
    uploaded = False

    try:
        # Initialize the S3 client
        s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name,
        )

        # Test 1: Check bucket connection by listing its settings
        print(f"Connecting to bucket '{bucket_name}'...")
        s3.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
        print("Success: Initial handshake completed.")

        # Test 2: Upload a dummy file to check write permissions
        print("Testing write permissions (uploading a test file)...")
        s3.put_object(
            Bucket=bucket_name,
            Key=test_file_key,
            Body="AWS S3 Connection test successful! The backend app can write to storage.",
            ContentType="text/plain",
        )
        uploaded = True
        print(f"Success: Uploaded '{test_file_key}' to S3.")

        print("\n=========================================")
        print("ALL S3 STORAGE TESTS PASSED SUCCESSFULLY!")
        print("=========================================")

    except NoCredentialsError:
        print("Error: Missing AWS credentials in your .env file.")
        sys.exit(1)
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials in your .env file.")
        sys.exit(1)
    except Exception as e:
        print(f"Error connecting to S3: {e}")
        sys.exit(1)
    finally:
        if uploaded and s3:
            try:
                s3.delete_object(Bucket=bucket_name, Key=test_file_key)
                print(f"[CLEANUP] Removed '{test_file_key}' from S3.")
            except Exception as error:
                print(f"[WARNING] S3 cleanup failed: {error}")


if __name__ == "__main__":
    run_tests()
