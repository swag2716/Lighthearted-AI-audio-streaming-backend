
import os
from boto3.session import Session
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError

try:
    load_dotenv()
    AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
    AWS_S3_REGION_NAME = os.environ["AWS_S3_REGION_NAME"]
    session = Session(region_name=AWS_S3_REGION_NAME,
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3 = session.resource('s3')
    bucket = s3.Bucket(AWS_STORAGE_BUCKET_NAME)
except KeyError as e:
    raise RuntimeError("Could not load AWS keys in environment") from e

def upload_to_s3(local_file, s3_file):

    try:
        with open(local_file, 'rb') as file:
            bucket.put_object(Key=s3_file, Body=file)
        return f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/{s3_file}"
    except NoCredentialsError:
        print("Credentials not available")
        return None