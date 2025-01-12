import time
import datetime
import paho.mqtt.client as mqtt
import ssl
import json
import _thread
import RPi.GPIO as GPIO
import pioamera
import boto3
import os 
import glob
from botocore.exceptions import NoCredentialsError

os.system('modprobe w1-gpio') 
os.system('modprobe w1-therm') 
  
base_dir = '/sys/bus/w1/devices/' 
device_folder = glob.glob(base_dir + '28*')[0] 
device_file = device_folder + '/w1_slave' 
  
#-------------------Camera--------------------  
#Pi camera image code 
def capture_image(file_path):
    with picamera.Picamera() as camera:
        camera.resoultion=(1024,768)
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


def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IoT: " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='./rootCA.pem', certfile='./certificate.pem.crt', keyfile='./private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("a3art0be4j4jr7-ats.iot.us-east-2.amazonaws.com", 8883, 60) #AWS IOT ->settings ->data Endpoint

def read_temp_raw(): 
    f = open(device_file, 'r') 
    lines = f.readlines() 
    f.close() 
    return lines 
def publishData(txt):
    print(txt)

    while (True):

        lines = read_temp_raw() 
        while lines[0].strip()[-3:] != 'YES': 
            time.sleep(0.2) 
            lines = read_temp_raw() 
        equals_pos = lines[1].find('t=') 
        if equals_pos != -1: 
            temp_string = lines[1][equals_pos+2:] 
            temp_c = float(temp_string) / 1000.0  
        return temp_c
        
        timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        #client.publish("raspi/data", payload=json.dumps({"distance": distance}), qos=0, retain=False)
        client.publish("raspb1/data", payload=json.dumps({"timestamp": timestamp, "Temperature": temp_c}), qos=0, retain=False)

        time.sleep(5)
 

def main():
    desktop_path="/home/nishi/iotfile"
    bucket="firedata1" #Enter bucket Name

    image_file_path=desktop_path+"cap.png"
    capture_image(image_file_path)
    upload_s3(image_file_path,bucket,"cap.png")
if _name=="main_":
    while(True):
        main()
        _thread.start_new_thread(publishData,("Spin-up new Thread...",))
        client.loop_forever()
