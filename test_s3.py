import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

print("=========================================")
print("NEUROPIX: Testing AWS S3 Storage...")
print("=========================================")

# Retrieve keys from environment
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket_name = os.getenv('AWS_BUCKET_NAME')
region_name = os.getenv('AWS_REGION')

try:
    # Initialize the S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region_name
    )
    
    # Test 1: Check bucket connection by listing its settings
    print(f"Connecting to bucket '{bucket_name}'...")
    s3.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
    print("Success: Initial handshake completed.")

    # Test 2: Upload a dummy file to check write permissions
    print("Testing write permissions (uploading a test file)...")
    test_file_name = "s3_test_connection.txt"
    s3.put_object(
        Bucket=bucket_name,
        Key=test_file_name,
        Body="AWS S3 Connection test successful! The backend app can write to storage.",
        ContentType="text/plain"
    )
    print(f"Success: Uploaded '{test_file_name}' to S3.")
    
    print("\n=========================================")
    print("ALL S3 STORAGE TESTS PASSED SUCCESSFULLY!")
    print("=========================================")

except NoCredentialsError:
    print("Error: Missing AWS credentials in your .env file.")
except PartialCredentialsError:
    print("Error: Incomplete AWS credentials in your .env file.")
except Exception as e:
    print(f"Error connecting to S3: {e}")