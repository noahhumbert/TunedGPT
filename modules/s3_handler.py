import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import requests

bucket_name = 'x1ai'
region_name = "us-east-2"
s3_client = boto3.client('s3', region_name=region_name)

# Get presigned URL for Upload to S3
def get_presigned_url_POST(object_name, expiration=3600):
    """
    Generate a presigned URL for uploading a file
    :param object_name: string, name of the object in S3
    :param expiration: Time in seconds for the presigned URL to remain valid (default is 1 hour)
    :return: Presigned POST as dictionary. If error, returns None.
    """
    s3_client = boto3.client('s3', region_name=region_name)

    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=None,
                                                     Conditions=None,
                                                     ExpiresIn=expiration)
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Error with credentials: {e}")
        return None
    except Exception as e:
        print(f"Could not generate presigned POST: {e}")
        return None

    return response

# Upload to S3
def upload_file_to_s3(file_path, object_name):
    """
    Upload a file to an S3 bucket using a pre-signed POST URL
    :param file_path: Local path to the file you want to upload
    :param object_name: S3 key (path) for the object in the bucket
    :return: None
    """
    # Get presigned URL for upload
    presigned_post = get_presigned_url_POST(object_name)

    if presigned_post is None:
        print("Could not generate presigned URL.")
        return

    # Read the file from local disk
    with open(file_path, 'rb') as file:
        files = {'file': (object_name, file)}

        # Send the file to S3 via the presigned POST URL
        try:
            response = requests.post(presigned_post['url'], data=presigned_post['fields'], files=files)
            
            if response.status_code == 204:
                print(f"File {file_path} successfully uploaded to {object_name} in S3.")
            else:
                print(f"Failed to upload file. Status code: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"Error during file upload: {e}")

# Get presigned URL to download from S3
def create_presigned_url_GET(object_name, expiration=3600):
    """
    Generate a presigned URL to share an S3 object
    :param object_name: string, name of the object in S3
    :param expiration: Time in seconds for the presigned URL to remain valid (default is 1 hour)
    :return: Presigned URL as string. If error, returns None.
    """
    s3_client = boto3.client('s3', region_name=region_name)

    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Error with credentials: {e}")
        return None
    except Exception as e:
        print(f"Could not generate presigned URL: {e}")
        return None

    return response

# Download from S3
def download_file_from_s3(object_name, local_file_path):
    """
    Download a file from S3 using a presigned URL
    :param object_name: string, S3 object key (path in S3 bucket)
    :param local_file_path: string, local path where the file will be saved
    :return: None
    """
    # Generate presigned URL
    presigned_url = create_presigned_url_GET(object_name)
    
    if presigned_url is None:
        print("Could not generate presigned URL.")
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
            print(f"File successfully downloaded from {object_name} to {local_file_path}.")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"Error during file download: {e}")