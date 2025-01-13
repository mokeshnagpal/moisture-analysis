from machine import Pin, ADC
import time


soil = ADC(Pin(34))
m = 100

min_moisture=0
max_moisture=4095

soil.atten(ADC.ATTN_11DB)       #Full range: 3.3v
soil.width(ADC.WIDTH_12BIT)     #range 0 to 4095


while True:
    try:
        soil.read()
        time.sleep(2)
        m = (max_moisture-soil.read())*100/(max_moisture-min_moisture)
        moisture = '{:.1f} %'.format(m)
        print('Soil Moisture:', moisture)
        time.sleep(5)
    except:
        pass