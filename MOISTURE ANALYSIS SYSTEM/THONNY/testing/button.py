from machine import Pin
from time import sleep
button = Pin(22, Pin.IN, Pin.PULL_UP)

while 1:
    print(button.value())
    sleep(1)