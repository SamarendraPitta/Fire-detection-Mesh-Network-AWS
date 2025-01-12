import time
import picamera
import datetime
import paho.mqtt.client as mqtt
import ssl
import json
import _thread
import boto3
from botocore.exceptions import NoCredentialsError
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(27,GPIO.IN)

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
#---------------------------------------------------------------------------
def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IoT: " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='./rootCA.pem', certfile='./certificate.pem.crt', keyfile='./private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("a3art0be4j4jr7-ats.iot.us-east-2.amazonaws.com", 8883, 60) #AWS IOT ->settings ->data Endpoint

def main():
    while True:
        desktop_path="/home/nishi11/Desktop/"
        bucket="firedata1" #Enter bucket Name
        for i in range(1,100000):
            image_file_path=desktop_path+"cap"+str(i)+".png"
            capture_image(image_file_path)
            upload_s3(image_file_path,bucket,"cap"+str(i)+".png")
            timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            client.publish("raspb1/data", payload=json.dumps({"timestamp": timestamp,"SMOKE":GPIO.input(27), "Temperature": 26.5}), qos=0, retain=False)
            try:
                if GPIO.input(27):
                    print("True")
                else:
                    print("Flase")
                time.sleep(5)
            finally:
                print("Complete")
            
    
main()
