# import test
import utime, time
import machine
from constants import *
from read_temp import read_temp, init_temp_sensor
from tools import Stepper, Button, Od, Peltier
import main_WEB
from main_WEB import client, mqtt_feedname_temperature, mqtt_feedname_OD

green_led = machine.Pin(LED_G_PIN, machine.Pin.OUT)
for i in range(3):
    green_led.value(1)
    utime.sleep(1)
    green_led.value(0)
    utime.sleep(1)
button = Button(BUTTON_PIN)
step_motor1 = Stepper(STP1_PIN, DIR1_PIN)
step_motor2 = Stepper(STP2_PIN, DIR2_PIN)
peltier_obj = Peltier(COOLING_PIN)
od_sensor1 = Od(LED_LIGHT_SENSOR_PIN, LIGHT_SENSOR_PIN)
temp_sens = init_temp_sensor(TENP_SENS_ADC_PIN_NO = 32)

while True:
    try:
        temp = read_temp(temp_sens)
        print(str(temp))
        client.publish(mqtt_feedname_temperature,
                       bytes(str(temp), 'utf-8'),
                       qos=0)
        od_measurement = od_sensor1.write_reading_sensor()
        print(str(od_measurement))
        client.publish(mqtt_feedname_OD,
                       bytes(str(od_measurement), 'utf-8'),
                       qos=0)


    except Exception as e: print(e)

    peltier_obj.cooler()
    #peltier_obj.even_cooler()
    step_motor1.rotate_some(1, 100)

    step_motor2.rotate_some(1, 100)

    green_led.value(1)
    if button.is_pressed():
       break
green_led.value(0)