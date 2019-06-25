# import test
import utime, time
import machine
from constants import *
from read_temp import read_temp, init_temp_sensor
from tools import Stepper, Button, Od, Peltier
import main_WEB
from PID import PID_Controller

from main_WEB import client, mqtt_feedname_temperature, mqtt_feedname_OD, mqtt_feedname_PID

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


wanted_temp = 19
pid_object = PID_Controller(P=0.2, I=1, D=1)

while True:
    try:
        temp = read_temp(temp_sens)
        # temp=23
        pid_object.update(temp - wanted_temp)
        PID_strength = pid_object.output
        client.publish(mqtt_feedname_temperature,
                       bytes(str(temp), 'utf-8'),
                       qos=0)
        od_measurement = od_sensor1.write_reading_sensor()
        print(od_measurement-800.0)
        client.publish(mqtt_feedname_OD,
                       bytes(str(od_measurement), 'utf-8'),
                       qos=0)
        client.publish(mqtt_feedname_PID,
                       bytes(str(PID_strength), 'utf-8'),
                       qos=0)

    except Exception as e: print(e)

    peltier_obj.even_cooler()
    #peltier_obj.even_cooler()

    pid_object.update(30 - wanted_temp)
    max_PID_Value = pid_object.output
    turns = int(100.0 * float(PID_strength) / float(max_PID_Value))
    print(PID_strength, temp, turns)

    '''
    if (temp)>wanted_temp:
    step_motor1.rotate_some(1, turns)

    else:
        step_motor1.rotate_some(1, 0)
    '''
    step_motor1.rotate_some(1, 3000)

    step_motor2.rotate_some(1, 3)

    green_led.value(1)
    if button.is_pressed():
       break
green_led.value(0)