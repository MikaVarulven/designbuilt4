from web_stuff import *
from PID import PID, map_action_to_steps
from read_temp import *
from tools import *
from constants import *

PUBLISH_PERIOD_IN_SEC = 10
SUBSCRIBE_CHECK_PERIOD_IN_SEC = 0.5
accum_time = 0

od_obj = Od(LED_LIGHT_SENSOR_PIN, LIGHT_SENSOR_PIN)

pump_water = Stepper(STP1_PIN, DIR1_PIN)
pump_algae = Stepper(STP2_PIN, DIR2_PIN)

green_led = machine.Pin(LED_G_PIN, machine.Pin.OUT)

button = Button(BUTTON_PIN)

# blink led 3 times just to check that everything is working so far.
for i in range(3):
    green_led.value(1)
    utime.sleep(1)
    green_led.value(0)
    utime.sleep(1)

P, I, D = 1, 1, 1

while True:
    try:
        # Publish
        if accum_time >= PUBLISH_PERIOD_IN_SEC:
            print('before temperature')
            temp = read_temp(temp_sens)
            print('after temperature')

            od_value = od_obj.get_OD_measurement()
            send_temperature(temp) #web
            send_od(od_value) # web
            accum_time = 0
            P, I, D = get_value(client_P, P), get_value(client_I, I), get_value(client_D, D) #get value from mqtt
            pid_object = PID(float(P), float(I), float(D))
            pid_object.SetPoint = 19
            print('after pid object')
            pid_object.update(temp)
            pid_action = pid_object.output
            number_steps = map_action_to_steps(pid_action)
            pump_water.rotate_some(1, number_steps)
            print(P, I, D )

        time.sleep(SUBSCRIBE_CHECK_PERIOD_IN_SEC)
        accum_time += SUBSCRIBE_CHECK_PERIOD_IN_SEC



    except Exception as e:
        print(str(e))
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()