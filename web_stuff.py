import network
import time
from robust import MQTTClient
import sys
import os
print('after imports')



'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
WIFI STUFF
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
'''


# turn off the WiFi Access Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("device")
#
# # WiFi connection information
# WIFI_SSID = 'device'
# WIFI_PASSWORD = 'designbuild4'
#
# # turn off the WiFi Access Point
# ap_if = network.WLAN(network.AP_IF)
# ap_if.active(False)
#
# # connect the device to the WiFi network
# wifi = network.WLAN(network.STA_IF)
# wifi.active(True)
# wifi.connect(WIFI_SSID)

# wait until the device is connected to the WiFi network
MAX_ATTEMPTS = 20
attempt_count = 0
while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
    attempt_count += 1
    time.sleep(1)

if attempt_count == MAX_ATTEMPTS:
    print('could not connect to the WiFi network')
    sys.exit()


print('After connecting to WIFI')

'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ADAFRUIT STUFF
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
'''
ADAFRUIT_IO_URL = b'io.adafruit.com'

ADAFRUIT_IO_USERNAME = b'eyyupoglu'
ADAFRUIT_IO_KEY = b'a8280cf83a7e455485c1c21c528acfec'

ADAFRUIT_IO_FEEDNAME_P = b'P_controller'
mqtt_feedname_P = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_FEEDNAME_P), 'utf-8')

ADAFRUIT_IO_FEEDNAME_I = b'I_controller'
mqtt_feedname_I = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_FEEDNAME_I), 'utf-8')

ADAFRUIT_IO_FEEDNAME_D = b'D_controller'
mqtt_feedname_D = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_FEEDNAME_D), 'utf-8')


# Define callback functions which will be called when certain events happen.
# def connected(client):
#     # Connected function will be called when the client is connected to Adafruit IO.
#     # This is a good place to subscribe to feed changes.  The client parameter
#     # passed to this function is the Adafruit IO MQTT client so you can make
#     # calls against it easily.
#     print('Connected to Adafruit IO!  Listening for {0} changes...'.format(ADAFRUIT_IO_FEEDNAME_TEMPERATURE))
#     # Subscribe to changes on a feed named DemoFeed.
#     client.subscribe(ADAFRUIT_IO_FEEDNAME_TEMPERATURE)

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))




'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
SETTING THE CALLBACKS AND INITIALIZING CLIENT
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
'''

# Create an MQTT client instance.

random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

client = MQTTClient(client_id=mqtt_client_id,
                    server=ADAFRUIT_IO_URL,
                    user=ADAFRUIT_IO_USERNAME,
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)


random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

client_P = MQTTClient(client_id=mqtt_client_id,
                    server=ADAFRUIT_IO_URL,
                    user=ADAFRUIT_IO_USERNAME,
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)


random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

client_I = MQTTClient(client_id=mqtt_client_id,
                    server=ADAFRUIT_IO_URL,
                    user=ADAFRUIT_IO_USERNAME,
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)


random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

client_D = MQTTClient(client_id=mqtt_client_id,
                    server=ADAFRUIT_IO_URL,
                    user=ADAFRUIT_IO_USERNAME,
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)

# Setup the callback functions defined above.
# client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

client_P.on_disconnect = disconnected
client_P.on_message    = message

client_I.on_disconnect = disconnected
client_I.on_message    = message

client_D.on_disconnect = disconnected
client_D.on_message    = message


# Connect to the Adafruit IO server.
client.connect()
client_P.connect()
client_I.connect()
client_D.connect()
print('after connect')

client.set_callback(message)
client_P.set_callback(message)
client_I.set_callback(message)
client_D.set_callback(message)

client_P.subscribe(mqtt_feedname_P)
client_I.subscribe(mqtt_feedname_I)
client_D.subscribe(mqtt_feedname_D)

def get_value(client, previous_value):
    value = None
    client.check_msg()
    value = client.latest_msg
    client.latest_msg = None

    if value ==None:
        value = previous_value
    return value
