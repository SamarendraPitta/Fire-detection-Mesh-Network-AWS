import time
import picamera
import boto3
from botocore.exceptions import NoCredentialsError

def capture_image(file_path):
    with picamera.PiCamera() as camera:
        camera.resolution=(1024,768)
        camera.capture(file_path)
def upload_s3(file_path,bucket,object):
    access_id=""
    secret_key=""
    s3=boto3.client('s3',aws_access_key_id=access_id,aws_secret_access_key=secret_key)

    try:
        s3.upload_file(file_path,bucket,object)
        print(f"File uploaded to S3: s3://{bucket}/{object}")

    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available or incorrect.")

desktop_path="/home/Desktop/"
bucket="firedata1" #Enter bucket Name

image_file_path=desktop_path+"cap.png"
capture_image(image_file_path)
upload_s3(image_file_path,bucket,"cap.png")
