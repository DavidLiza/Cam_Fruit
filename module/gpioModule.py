#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__  = "David Lizarazo"
__version__ ="1.0.0"

"""Este programa usa los 
GPIO para enceder perifericos necesario
para el desarrollo del presente proyeto """

from num2words import num2words
from subprocess import call
import RPi.GPIO as GPIO
import time

# GPIO RASP BOARD ( Common PINS with ZERO, PI 2 , PI 4	)
PIN_BUZZER= 17
PIN_GREEN = 27
PIN_RED   = 22
PIN_BLUE  = 23
# Logica vairables used depends in the electronic USED
PIN_ON     =  True
PIN_OFF    =  False

#set Ultrasonic GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 7


def GPIO_CONF(LOGIC_ON='HIGH'):
    global PIN_ON
    global PIN_OFF
    if LOGIC_ON == 'LOW' or LOGIC_ON=='low' or LOGIC_ON=='Low':
        PIN_ON = False
        PIN_OFF= True
    #Disable warning pins
    GPIO.setwarnings(False)
    

    #GPIO Mode (BOARD / BCM)
    #GPIO.setmode(GPIO.BOARD) # Set the pins as hardware pins are nummerated (Left odds)
    GPIO.setmode(GPIO.BCM) # para Ultrasonido 


    #Enable the pins to be used and set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    GPIO.setup (PIN_GREEN , GPIO.OUT)
    GPIO.setup (PIN_RED   , GPIO.OUT)
    GPIO.setup (PIN_BUZZER, GPIO.OUT)
    GPIO.setup (PIN_BLUE  , GPIO.OUT)

    GPIO.output(PIN_BLUE , PIN_OFF)
    GPIO.output(PIN_RED  , PIN_OFF)
    GPIO.output(PIN_GREEN, PIN_OFF)
    GPIO.output(PIN_BUZZER, False)

def GPIO_INIT ():
    GPIO.output(PIN_BLUE , PIN_OFF  )
    GPIO.output(PIN_GREEN ,PIN_ON   )
    GPIO.output(PIN_BUZZER,GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(PIN_BUZZER,GPIO.LOW )
    time.sleep(0.3)
    GPIO.output(PIN_BUZZER,GPIO.HIGH)
    GPIO.output(PIN_RED   ,PIN_ON   )
    time.sleep(0.3)
    GPIO.output(PIN_BUZZER,GPIO.LOW )
    GPIO.output(PIN_RED   ,PIN_OFF  )
    time.sleep(0.3)
    GPIO.output(PIN_GREEN ,PIN_OFF  )
    GPIO.output(PIN_BUZZER,GPIO.LOW )
    GPIO.output(PIN_BLUE , PIN_ON   )

def GPIO_PROC_OFF():
    try:
            GPIO.output(PIN_RED, PIN_ON     )
            GPIO.output(PIN_BUZZER,GPIO.HIGH)
            time.sleep(0.3)
            GPIO.output(PIN_BUZZER,GPIO.LOW )
            time.sleep(0.3)
            GPIO.output(PIN_RED, PIN_OFF    )
            GPIO.output(PIN_BUZZER,GPIO.HIGH)
            GPIO.output(PIN_GREEN ,PIN_ON)
            time.sleep(0.3)
            GPIO.output(PIN_BUZZER,GPIO.LOW )
            GPIO.output(PIN_GREEN ,PIN_OFF  )
            GPIO.output(PIN_RED, PIN_ON     )
            time.sleep(0.3)
            GPIO.output(PIN_RED   ,PIN_OFF  )
            GPIO.output(PIN_BUZZER,GPIO.LOW )
            GPIO.output(PIN_BLUE  ,PIN_OFF)
            GPIO.cleanup()
    except Exception as e:
            print ("Couldnt Open the GPIOs, probably were closed before")

def GPIO_ACCEPTED():
    GPIO.output(PIN_BLUE , PIN_OFF  )
    GPIO.output(PIN_BUZZER,GPIO.HIGH)
    GPIO.output(PIN_GREEN ,PIN_ON   )
    time.sleep(0.3)
    GPIO.output(PIN_GREEN ,PIN_OFF  )
    GPIO.output(PIN_BUZZER,GPIO.LOW )
    GPIO.output(PIN_BLUE , PIN_ON   )

def GPIO_REJECT():
    GPIO.output(PIN_BLUE , PIN_OFF  )
    GPIO.output(PIN_RED   ,PIN_ON   )
    GPIO.output(PIN_BUZZER,GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(PIN_RED   ,PIN_OFF  )
    GPIO.output(PIN_BUZZER,GPIO.LOW )
    GPIO.output(PIN_BLUE , PIN_ON   )

def get_distance():
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        # Init time
        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s) and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        if distance < 400 :
            return distance
        return None


# --------------------- TESTS -----------------------
def ultrasonic_test():
    try:
        while True:
            dist = get_distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()



def main_test():
    print("** GPIO TEST **")
    #GPIO_CONF('LOW')
    GPIO_CONF('HIGH')
    GPIO_INIT()
    GPIO_INIT()
    print("** DONE WITH THE PROCESS **")
    GPIO.cleanup()


if __name__ == '__main__':
    GPIO_CONF('HIGH')
    
    try:
        while True:
            dist = get_distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

    main()
