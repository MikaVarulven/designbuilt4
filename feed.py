from constants import *
from tools import Od, Stepper


pump_algae = Stepper(STP2_PIN, DIR2_PIN)

def feed():

    #assumes theres liquid in the tube
    od_value = Od.get_OD_measurement()

    #concentration of the algae solution
    concentration = get_concentration(od_value)

    #450 turns translates to 1 ml roughly
    #feed 3 ml
    pump_algae.rotate_some(0, 1350)

def feed_initial():
    
    # assumes theres liquid in the tube
    od_value = Od.get_OD_measurement()

    # concentration of the algae solution
    concentration = get_concentration(od_value)

    # 450 turns translates to 1 ml roughly
    # feed 12 ml
    pump_algae.rotate_some(0, 5400)


def get_concentration(od_value):
    #od vs cell count needs to be calibrated
    return 0


def prepump():
    #need to measure how many turns pump the water to the sensor
    pump_algae.rotate_some(0, 1000)

#code that should go in main while loop
'''
prepump()
feed_initial()
last_fed = utime.time()
    
feeding_period = 1500 #25 minutes
if utime.time() - last_fed >= feeding_period:
    feed()
    last_fed = utime.time()
'''





