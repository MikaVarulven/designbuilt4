import machine
import time
from constants import *


class Stepper(object):
    def __init__(self, step_pin, dir_pin):
        # to_log('init ko')
        self.stp = machine.Pin( step_pin, machine.Pin.OUT)
        self.dir = machine.Pin( dir_pin, machine.Pin.OUT)
        # to_log('init ok')


    def rotate_some(self, dir, times):
        '''
        :param dir:
        :return:
        '''
        print('it works')

        self.dir.value(dir)
        print('it works2')

        for i in range(0,times):
            print('it works3')

            self.stp.value(1)
            # to_log(1)
            print('it works4')

            time.sleep(0.001)
            print('it works5')

            self.stp.value(0)
            print('it works6')

            # to_log(2)
            time.sleep(0.001)
            print('it works7')

    def rotate_one_step(self, dir):
        '''
        :param dir:
        :return:
        '''

        print('it works')
        self.dir.value(dir)
        print('it works2')

        self.stp.value(1)
        print('it works3')

        time.sleep(0.0001)
        print('it works4')

        self.stp.value(0)
        print('it works5')

        time.sleep(0.0001)
        print('it works')


def to_log( str_, file_name='text.txt' ):
    file = open(file_name, 'a')
    file.write(' : ' + str(str_)+'\n')
    file.close()

class Button(object):
    def __init__(self, pin):
        self.button = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        # to_log('init fine button')

    def is_pressed(self):
        return (0==self.button.value())


class Od(object):
    def __init__(self, led_pin, os_pin):
        self.od_led = machine.PWM(machine.Pin(led_pin), freq=78000)
        self.sensor = machine.ADC(machine.Pin(os_pin))
        # set attenuation at 11db
        self.sensor.atten(3)
        # set width to 11 bit
        self.sensor.width(3)

        # Creates a writeable text file
        self.f = open('fixedPWM.txt', 'w')
        self.f.write('FIXED_PWM_VALUE\n')
        self.f.close()


    def write_reading_sensor(self):

        # opening the text file
        self.f = open('fixedPWM.txt', 'a+')

        self.od_led.duty(200)
        # self.od_led.duty(0)

        avgReading = 0
        for j in range(50000):
            avgReading += self.sensor.read()
        x = str(avgReading / 50000)
        self.f.write(x + ',')

        self.f.close()


    # def run():
    #
    #
    #     # print(sensor.read())
    #
    #     for i in range(100):
    #         led.duty(200)
    #         time.sleep_ms(30)
    #         avgReading = 0
    #         for j in range(50000):
    #             avgReading += sensor.read()
    #         x = str(avgReading / 50000)
    #         print(x)
    #         f.write(x + ',')
    #
    #     f.close()



'''
DELETE THIS
'''

# # 12 is step, 13 is dir
#
# step_motor = Stepper(12, 13)
#
# step_motor.rotate_some(1)
