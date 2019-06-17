# import test
import utime
import machine
from constants import *
#from read_temp import *
from tools import Stepper, Button, Od, Peltier
# to_log


# file = open('text.txt', 'w')
# file.write('smt')
# file.close()

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


# step_motor2 = Stepper(STP2_PIN, DIR2_PIN)
# # step_motor2.rotate_some(0)
#
#od_sensor1 = Od(LED_LIGHT_SENSOR_PIN, LIGHT_SENSOR_PIN)
print('here')
# to_log('fine after init')


#temp_sens = init_temp_sensor()



while True:
    print('while')
   # temp = read_temp(temp_sens)
    #print(str(temp))
# if statment about the dif between temps

    peltier_obj.cooler()
    step_motor1.rotate_some(1, 10)
    step_motor1.rotate_some(0, 10)
    peltier_obj.even_cooler()
    step_motor2.rotate_some(1, 10)
    step_motor2.rotate_some(0, 10)
    #od_sensor1.write_reading_sensor()
    # time.sleep(0.1)
    if button.is_pressed():
       break




green_led.value(1)


# while True:
#     if button.is_pressed():
#         green_led.value(0)
#         break
#     else:
#         green_led.value(1)
#         # time.sleep(2.0)
#         # print(button.value())
#         # while not button.is_pressed():
#         #     green_led.value(1)
#         #     time.sleep(0.1)
#         #     green_led.value(0)
#         #     time.sleep(0.1)
#         #     to_log('the led should be on')
