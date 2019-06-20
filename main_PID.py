from web_stuff import *
from PID import PID
from read_temp import *
from constants import *
from tools import *
from machine import *

#initialize stepper motor & Peltier Element
stepper1 = Stepper(STP1_PIN, DIR1_PIN)
peltier1 = Peltier(COOLING_PIN)

#set web constants
PUBLISH_PERIOD_IN_SEC = 10
SUBSCRIBE_CHECK_PERIOD_IN_SEC = 0.5
accum_time = 0

#set PID constants
P, I, D = 1, 0, 0

#define PID object with PID constants
pid_object = PID(float(P), float(I), float(D))

#updating constants from the web if necessary
P, I, D = get_value(client_P, P), get_value(client_I, I), get_value(client_D, D)
pid_object.setKp(P)
pid_object.setKi(I)
pid_object.setKd(D)

#cooling while loop
while True:
    try:
        # Publish
        if accum_time >= PUBLISH_PERIOD_IN_SEC:
            # print('Publish:  freeHeap = {}'.format(free_heap_in_bytes))
            # client.publish(mqtt_feedname_temperature,
            #                bytes(str(free_heap_in_bytes), 'utf-8'),
            #                qos=0)
            accum_time = 0

        #read temp
        temp = read_temp(temp_sens)
        print('after temp sensor')


        #feed temp from sensor to PID
        print('after pid object')
        pid_object.update(temp)


        #store output of pID in action variable
        pid_action = pid_object.output

        #action of steppermotor depending on intensity
        if -5 <= pid_action <= -4:
            PWM(stepper1, round(pid_action))
        elif -4 < pid_action <= -2:
            PWM(stepper1, round(pid_action))


        print('action: %s' %pid_action)
        print('p: %s' %P)
        print('i: %s' %I)
        print('d: %s' %D)

        print(P, I, D )

        time.sleep(SUBSCRIBE_CHECK_PERIOD_IN_SEC)
        accum_time += SUBSCRIBE_CHECK_PERIOD_IN_SEC

        print('end while loop')

    except Exception as e:
        print(str(e))
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()