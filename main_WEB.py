
import time
from robust import MQTTClient
import os
import gc
import sys
from read_temp import *
import network


# WiFi connection information
WIFI_SSID = 'Iphone'
WIFI_PASSWORD = 'mikemike'

# turn off the WiFi Access Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)


# wait until the device is connected to the WiFi network
MAX_ATTEMPTS = 20
attempt_count = 0
while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
    attempt_count += 1
    time.sleep(1)

if attempt_count == MAX_ATTEMPTS:
    print('could not connect to the WiFi network')
    sys.exit()

# create a random MQTT clientID
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')


ADAFRUIT_IO_URL = b'io.adafruit.com'
ADAFRUIT_USERNAME = b'eyyupoglu'
ADAFRUIT_IO_KEY = b'a8280cf83a7e455485c1c21c528acfec'
ADAFRUIT_IO_FEEDNAME_TEMPERATURE = b'temperature'
ADAFRUIT_IO_FEEDNAME_OD_SENSOR = b'OD_sensor'

client = MQTTClient(client_id=mqtt_client_id,
                    server=ADAFRUIT_IO_URL,
                    user=ADAFRUIT_USERNAME,
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)
try:
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

mqtt_feedname_temperature = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME_TEMPERATURE), 'utf-8')
mqtt_feedname_OD = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME_OD_SENSOR), 'utf-8')
PUBLISH_PERIOD_IN_SEC = 10


def do_subscribed(topic, msg):
    print((topic, msg))

temp = 8888




"""

try:
    temp_sens = init_temp_sensor()
except:
    temp = 1
while True:
    try:
        try:
            temp = read_temp(temp_sens)
        except:
            temp = 2
        client.publish(mqtt_feedname,    
                   bytes(str(temp), 'utf-8'),
                   qos=0)
        #client.set_callback(do_subscribed)
        #client.subscribe(topic="Mika007/feeds/Temperature")
        time.sleep(PUBLISH_PERIOD_IN_SEC)
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()


"""