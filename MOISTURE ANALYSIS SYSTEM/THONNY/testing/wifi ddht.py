from network import STA_IF,WLAN
from time import sleep, sleep_us, ticks_us, time
import ufirebase as f
from machine import Pin, ADC
from dht import DHT22
from json import dumps, loads
from urequests import post

valve = Pin(4, Pin.OUT)
pump = Pin(15, Pin.OUT) 
trigger = Pin(19, Pin.OUT)
echo = Pin(18, Pin.IN)
button = Pin(22, Pin.IN, Pin.PULL_UP)
sensor = DHT22(Pin(2))
soil = ADC(Pin(34,mode=Pin.IN))
soil.atten(ADC.ATTN_11DB)      
soil.width(ADC.WIDTH_12BIT)
temp_power = Pin(21, Pin.OUT)

valve.off()
pump.off()

ssid = 'MAJESTIC MOKSH'
password = 'Mokesh87654321'
def connect():
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)        
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
connect()


firebase_url = "https://soil-moisture-analysis-default-rtdb.asia-southeast1.firebasedatabase.app/"
server_url = "https://moisture-prediction.onrender.com/predict"

while 1:
    try:
        sensor.measure()
        temp = sensor.temperature()
        temp_f = temp * (9/5) + 32.0
        print(temp)
    except Exception as e:
        pass
    