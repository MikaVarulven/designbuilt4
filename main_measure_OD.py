# import test
import time
import machine
from constants import *
from tools import Stepper, Button, Od
# to_log


# file = open('text.txt', 'w')
# file.write('smt')
# file.close()

green_led = machine.Pin(LED_G_PIN, machine.Pin.OUT)
# for i in range(3):
#     green_led.value(1)
#     time.sleep(1)
#     green_led.value(0)
#     time.sleep(1)

button = Button(BUTTON_PIN)
while not button.is_pressed():
    time.sleep(0.1)

# while True:
#     if button.is_pressed():
#         break

step_motor1 = Stepper(STP1_PIN, DIR1_PIN)
step_motor1.rotate_some(1,5000)

# step_motor2 = Stepper(STP2_PIN, DIR2_PIN)
# # step_motor2.rotate_some(0)
#
od_sensor1 = Od(LED_LIGHT_SENSOR_PIN, LIGHT_SENSOR_PIN)
print('here')
# to_log('fine after init')





while True:

    step_motor1.rotate_some(1, 500)
    od_sensor1.write_reading_sensor()
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
