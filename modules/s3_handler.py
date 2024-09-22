# Handles S3 requests including getting upload/download urls and uploading/downloading with S3
# Takes the local path of either the destination or the path to pull as well as the bucket location
# Outputs whatever your heart desires

# IMPORTS
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import requests

# Initialize Bucket
bucket_name = 'x1ai'
region_name = "us-east-2"
s3_client = boto3.client('s3', region_name=region_name)

# Get presigned URL for Upload to S3
def get_presigned_url_POST(object_name, expiration=3600):
    s3_client = boto3.client('s3', region_name=region_name)

    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=None,
                                                     Conditions=None,
                                                     ExpiresIn=expiration)
    except (NoCredentialsError, PartialCredentialsError) as e:
        return None
    except Exception as e:
        return None

    return response

# Upload to S3
def upload_file_to_s3(file_path, object_name):
    # Get presigned URL for upload
    presigned_post = get_presigned_url_POST(object_name)

    if presigned_post is None:
        return

    # Read the file from local disk
    with open(file_path, 'rb') as file:
        files = {'file': (object_name, file)}

        # Send the file to S3 via the presigned POST URL
        try:
            response = requests.post(presigned_post['url'], data=presigned_post['fields'], files=files)
        except Exception as e:
            print(f"Error during file upload: {e}")

# Get presigned URL to download from S3
def create_presigned_url_GET(object_name, expiration=3600):
    s3_client = boto3.client('s3', region_name=region_name)

    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except (NoCredentialsError, PartialCredentialsError) as e:
        return None
    except Exception as e:
        return None

    return response

# Download from S3
def download_file_from_s3(object_name, local_file_path):
    # Generate presigned URL
    presigned_url = create_presigned_url_GET(object_name)
    
    if presigned_url is None:
        return
    
    # Download the file using the presigned URL
    try:
        response = requests.get(presigned_url, stream=True)
        
        if response.status_code == 200:
            # Write the file to the local file path
            with open(local_file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # Filter out keep-alive new chunks
                        file.write(chunk)
    except Exception as e:
        print(f"Error during file download: {e}")