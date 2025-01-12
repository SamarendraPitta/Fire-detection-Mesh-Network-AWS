#import time
#from w1thermsensor import W1ThermSensor
#sensor=W1ThermSensor()
#while True:
#    temp=sensor.get_temperature()
#   print(temp)
#   time.sleep(5)
#Libraries
import Adafruit_DHT
import board
from time import sleep
dht=Adafruit_DHT.DHT22(board.D4)
#Set DATA pin
#DHT = 4
while True:
    #Read Temp and Hum from DHT22
    temp=dht.temperature
    #h,t = dht.read_retry(dht.DHT22, DHT)
    #Print Temperature and Humidity on Shell window
    #print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t,h))
    print(temp)
    sleep(5) #Wait 5 seconds and read again
