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


try:
    sensor.measure()
    temp = sensor.temperature()
    temp_f = temp * (9/5) + 32.0
    if(temp == 0):
        temp =25
    print("Temperature",temp)
except Exception as e:
    pass
f.setURL(firebase_url)
f.get("","data",bg=0)
f.put("change", 0, bg=0)


min_moisture=0
max_moisture=4095
old_distance = 0.0
original_height = f.data["original_height"]
m = 100
temp =25
temp_f= 75
payload = { 
    "pH": f.data['ph'],
    "Soil EC": f.data['soil_ec'],
    "Phosphorus": f.data['phosphorus'],
    "Potassium": f.data['potassium'],
    "Urea": f.data['urea'],
    "T.S.P": f.data['tsp'],
    "M.O.P": f.data['mop'],
    "Temperature": temp_f,
    "Plant Type": f.data['plant_type']
}

for i,j in payload.items():
    if(isinstance(j, (int,float))==False):
        payload[i] = 0
        f.put(i, 0, bg = 0)
payload_json = dumps(payload)
response = loads(post(server_url, json=payload_json).text)['moisture_prediction'][0]

def ultra():
    global old_distance
    trigger.value(0)
    sleep_us(2)
    trigger.value(1)
    sleep_us(5)
    trigger.value(0)
    signaloff = signalon = 0
    while echo.value() == 0:
        signaloff = ticks_us()
    while echo.value() == 1:
        signalon = ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    distance = round(distance,2)
    if(distance>200 or distance<0):
        distance = 0
    if(old_distance != distance):
        old_distance = distance
    if(button.value() == 0):
        f.put('original_height', old_distance, bg=0)
        original_height = old_distance
    sleep(2)
temp =25
temp_f=75
while True:
    ultra()
    print("Maximum of container",original_height)
    print("Current height of container",old_distance)
    if(original_height - old_distance < 2):
        pump.value(1)
        while(old_distance > 5):
            ultra()
        pump.value(0)
        
        
    soil_value = soil.read()
    try:
        sensor.measure()
        temp = sensor.temperature()
        temp_f = temp * (9/5) + 32.0
        print("Temperature",temp)
        if(temp == 0):
            temp =25
    except Exception as e:
        pass
    m = (max_moisture-soil_value)*100/(max_moisture-min_moisture)
    moisture = '{:.1f} %'.format(m)
    moisture = float(moisture.replace('%', '', 1))


    f.get("change","data",bg=0)
    
    if(f.data):
        
        f.get("","data",bg=0)
        valve.value(f.data["override"])
    
        payload_send = 0
        if(f.data["override"] == 0 & temp_old != temp_f ):
            payload["Temperature"] = temp_f    
            payload_send = 1 
          
      
        if(f.data["override"] == 0 & data == 1):
            f.get("", "data", bg=0)
            payload["Phosphorus"] = f.data['phosphorus']
            payload["Potassium"] = f.data['potassium']
            payload["Urea"] = f.data['urea']
            payload["T.S.P"] = f.data['tsp']
            payload["M.O.P"] = f.data['mop']
            payload["Soil EC"] = f.data['soil_ec']
            payload["plant_type"] = f.data['plant_type']
            payload["pH"] = f.data['ph']
            payload_send = 1
        
    
        if(payload_send == 1):
            payload_json = dumps(payload)
            response = loads(post(server_url, json=payload_json).text)['moisture_prediction'][0]
            
            
            f.put("change", 0, bg=0)
            payload_send = 0
    print("Moisture current",moisture)
    print("Moisture predicted",response)
    if(moisture<response):
        valve.value(1)
        while (moisture<response):
            ultra()
        valve.value(0)
    f.put('moisture_value', moisture, bg=0)  #put this inside loop
    sleep(10)

        


