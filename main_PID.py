from web_stuff import *
from PID import PID
from read_temp import *



PUBLISH_PERIOD_IN_SEC = 10
SUBSCRIBE_CHECK_PERIOD_IN_SEC = 0.5
accum_time = 0



P, I, D = 1, 1, 1

while True:
    try:
        # Publish
        if accum_time >= PUBLISH_PERIOD_IN_SEC:
            # print('Publish:  freeHeap = {}'.format(free_heap_in_bytes))
            # client.publish(mqtt_feedname_temperature,
            #                bytes(str(free_heap_in_bytes), 'utf-8'),
            #                qos=0)
            accum_time = 0

            # Subscribe.  Non-blocking check for a new message.

        temp = read_temp(temp_sens)
        print('after temp sensor')

        P, I, D = get_value(client_P, P), get_value(client_I, I), get_value(client_D, D)
        pid_object = PID(float(P), float(I), float(D))
        print('after pid object')
        pid_object.update(24)

        pid_action = pid_object.output

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