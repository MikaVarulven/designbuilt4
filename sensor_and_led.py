from machine import PWM , ADC , Pin
import time
import math

def run():

    # creates a PWM instance (led) at pin number 32 and with a max frequency of 7800
    led = PWM( Pin( 32 ) , freq = 78000)
   
    # creates a ADC instance (sensor) at analogue pin A4 or pin number 36
    sensor = ADC( Pin( 36 ) )
    # set attenuation at 11db
    sensor.atten(3)
    #set width to 11 bit
    sensor.width(3)

    # Creates a writeable text file
    f = open('fixedPWM.txt','w')
    f.write('FIXED_PWM_VALUE\n')
    
    print(sensor.read())

    for i in range (100):
        led.duty(200)
        time.sleep_ms(30)
        avgReading = 0
        for j in range(50000):
            avgReading += sensor.read()
        x= str(avgReading/50000)
        print(x)
        f.write( x + ',' )

    f.close()

run()
