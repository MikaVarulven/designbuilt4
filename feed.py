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


def get_concentration(od_value):
    #od vs cell count needs to be calibrated
    pass


def prepump():
    #need to measure how many turns pump the water to the sensor
    pump_algae.rotate_some(0, 1000)



