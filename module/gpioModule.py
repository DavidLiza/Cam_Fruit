#!/usr/bin/env python
# -*- coding: utf-8 -*-
_author_= "David Lizarazo"
_version_="1.0.0"

"""Este programa usa los 
GPIO para enceder dos leds 
y un buzzer """

from num2words import num2words
from subprocess import call
import RPi.GPIO as GPIO
import time

# GPIO RASP BOARD ( Common PINS with ZERO, PI 2 , PI 4	)
PIN_BUZZER= 11
PIN_GREEN = 13
PIN_RED   = 15
PIN_BLUE  = 16
# Logica vairables used depends in the electronic USED
PIN_ON     =  True
PIN_OFF    =  False

def GPIO_CONF(LOGIC_ON='HIGH'):
    global PIN_ON
    global PIN_OFF
    if LOGIC_ON == 'LOW' or LOGIC_ON=='low' or LOGIC_ON=='Low':
        PIN_ON = False
        PIN_OFF= True
    #Disable warning pins
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) # Set the names as GPIOS and no BOARDS

    #Enable the pins to be used
    GPIO.setup (PIN_GREEN , GPIO.OUT)
    GPIO.setup (PIN_RED   , GPIO.OUT)
    GPIO.setup (PIN_BUZZER, GPIO.OUT)
    GPIO.setup (PIN_BLUE  , GPIO.OUT)

    GPIO.output(PIN_BLUE , PIN_OFF)
    GPIO.output(PIN_RED  , PIN_OFF)
    GPIO.output(PIN_GREEN, PIN_OFF)

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


def GPIO_READ():
    GPIO.output(PIN_BLUE , PIN_OFF  )
    GPIO.output(PIN_BUZZER,GPIO.HIGH)
    GPIO.output(PIN_GREEN ,PIN_ON   )
    GPIO.output(PIN_RED   ,PIN_ON   )
    time.sleep(0.3)
    GPIO.output(PIN_BUZZER,GPIO.LOW )
    GPIO.output(PIN_GREEN ,PIN_OFF  )
    GPIO.output(PIN_RED   ,PIN_OFF  )
    GPIO.output(PIN_BLUE , PIN_ON   )

def main():
    print("** GPIO TEST **")
    #GPIO_CONF('LOW')
    GPIO_CONF('HIGH')
    GPIO_INIT()
    GPIO_INIT()
    print("** DONE WITH THE PROCESS **")
    GPIO.cleanup()


if __name__ == '__main__':
    main()
