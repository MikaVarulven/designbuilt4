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

peltier1 = Peltier(COOLING_PIN)

green_led = machine.Pin(LED_G_PIN, machine.Pin.OUT)

button = Button(BUTTON_PIN)


def set_frequency_with_pid(pid_action):
    if pid_action < -5:
        print('inside zero if. before PWM')
        pump_water.set_freq(1000)
        peltier1.even_cooler()
        print('inside zero if. after PWM')
    elif -5 <= pid_action <= -4:
        print('inside first if. before PWM')
        pump_water.set_freq(700)
        peltier1.even_cooler()
        print('inside first if. after PWM')
    elif -4 < pid_action <= -2:
        print('inside second if. before PWM')
        pump_water.set_freq(500)
        peltier1.cooler()
        print('inside second if. after PWM')
    elif -2 < pid_action <= 0:
        print('inside third if. before PWM')
        pump_water.set_freq(350)
        peltier1.cooler()
        print('inside third if. after PWM')




# blink led 3 times just to check that everything is working so far.
for i in range(3):
    green_led.value(1)
    utime.sleep(1)
    green_led.value(0)
    utime.sleep(1)

P, I, D = 1, 0, 0

while True:
    try:
        # Publish
        if accum_time >= PUBLISH_PERIOD_IN_SEC:
            print('before temperature')
            temp_sens = init_temp_sensor()
            temp = read_temp(temp_sens)
            print('after temperature')





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
            # pump_water.rotate_some(1, number_steps)
            print(P, I, D )
            print('pid action: %s' %pid_action )

            # action of steppermotor depending on intensity
            set_frequency_with_pid(pid_action)



        time.sleep(SUBSCRIBE_CHECK_PERIOD_IN_SEC)
        accum_time += SUBSCRIBE_CHECK_PERIOD_IN_SEC

        if button.is_pressed():
            break




    except Exception as e:
        print(str(e))
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()


green_led.value(1)


