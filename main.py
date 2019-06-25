from PID import PID
from tools import *
from constants import *
import utime
from read_temp import *
from web_stuff import *


pump_water = StepperPWM(STP1_PIN, DIR1_PIN)
pump_water.set_dir(1)
pump_water.set_freq(0)
pump_water.set_duty(0)
pump_algae = Stepper(STP2_PIN, DIR2_PIN)

green_led = machine.Pin(LED_G_PIN, machine.Pin.OUT)

button = Button(BUTTON_PIN)

peltier1 = Peltier(COOLING_PIN)
peltier1.cooler()


print('After imports')

#
# text_file_od = 'od.txt'
#
# text_file = open(text_file_od, 'w')
# text_file.write('OD \n')
# text_file.close()


P, I, D = 1, 0, 0

pid_object = PID(float(P), float(I), float(D))

while True:
    if button.is_pressed():
        break

def pid_map_freq(pid_action):
    if pid_action >= 0:
        peltier1.cooler()
        pump_water.set_duty(0)
    elif pid_action < 10:
        peltier1.even_cooler()
        pump_water.set_duty(200)
        # pump_water.set_freq(int(-pid_action*100))
        pump_water.set_freq(350)

while True:
    pump_algae.rotate_some(1,100)
    if button.is_pressed():
        break


P, I, D = 1, 0, 0

last_minute = time.localtime()[4] - 1
while True:

    handle_wifi(wifi, client_P, client_I, client_D, client)

    # water pump - for some reason, does not work outside the while loop




    # pump_algae.rotate_some(1, 100)

    green_led.value(1)
    utime.sleep(0.5)
    green_led.value(0)
    utime.sleep(0.5)

    # temperature
    temp_sens = init_temp_sensor()
    temp = read_temp(temp_sens)


    # pid
    pid_object.SetPoint = 12
    pid_object.update(temp)




    P, I, D = get_value(client_P, P), get_value(client_I, I), get_value(client_D, D)
    pid_action = pid_object.output
    pump_water.map_action_to_frequency(pid_action, peltier1)
    pump_water.set_dir(1)
    print('P: %s\tI: %s\tD: %s' %(P, I, D))
    print('pid action: %s' % pid_action)


    # od measurements
    pump_algae.rotate_some(1, 1000)

    pump_water.set_duty(512)


    if send_data_adafruit(last_minute)[0]:
        od_obj = Od(LED_LIGHT_SENSOR_PIN,
                    LIGHT_SENSOR_PIN)  # if moved, it changes the bit resolution of the measurement
        od_obj.set_duty(7)
        od_value = od_obj.get_OD_measurement()
        print('od value: %s \n\n' % (od_value))
        last_minute = send_data_adafruit(last_minute)[1]
        send_temperature(temp)
        send_od(od_value)
        send_PID_action(pid_action)



    if button.is_pressed():
        break

green_led.value(0)
pump_water.set_duty(0)