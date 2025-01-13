from machine import Pin, ADC
from time import sleep, sleep_us, ticks_us, time

trigger = Pin(19, Pin.OUT)
echo = Pin(18, Pin.IN)

old_distance = 0

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
        print(distance)

while True:
    ultra()
    sleep(2)
