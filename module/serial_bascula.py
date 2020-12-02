#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__     = "David Lizarazo"
__copyright__  = "Copyright 2020"
__credits__    = ["David Lizarazo"]
__license__    = "GPL"
__version__    = "1.0.0"
__maintainer__ = "David Lizarazo"
__status__     = "Production"

import json 
import time
import serial
from threading import Thread

try: 
    import module.log           as log
    import module.constants     as CONS
    import module.decodeModule  as DEC

except Exception as e:
    import log
    import constants        as CONS
    import decodeModule     as DEC

logger = log.configure_logger('default')
"""
PINOUT MODULE 
(Gpios Pin Fisicos)
8   - Tx a Rx Bascula 
10  - Rx a Tx Bascula

"""

class Just_Read ():

    def __init__(self,speed = 9600 , port = 'ttyAMA0' ):
        self.__speed = speed
        self.__port  = '/dev/'+ port
        self.__isRun = False
        self.__wdec  = True
        try:
            self._serial   = serial.Serial(self.__port, self.__speed , timeout=5 )
            self.__isRun = True
        except Exception as e:
            print ("Error {}".format(e))
            #logger.info('OJE008 INIT_CONNECTION ')
            self.__isRun = False
            self._serial = False


    @property
    def port(self):
        return self._port
    
    @property
    def speed(self):
        return self.__speed
    
    @property
    def isRun(self):
        return self.__isRun

    def __del__(self):
        self.__isRun = False

    def ver_serial(self):
        if self._data != None :
            self._did_read = False
        
        #else:
        #   self._did_read = DEC.NOT_PROT
        pass

    def rec(self):
        """
        This function enter a While loop until some data is read.
        @returns It can return False in case that a QR with no protocol was read 
                 or the Data in a Dict if the protocol is acomplished
        """
        print (CONS.bcolors.HEADER+"Lectura Serial"+CONS.bcolors.ENDC)

        self._serial.reset_input_buffer()
        self._serial.reset_output_buffer()
        self._serial.set_input_flow_control(True)
        
        self._did_read = False
        
        #try:
        while self.__isRun:
                self._data=self._serial.read() 
                #x = ser.read()          # read one byte
                #s = ser.read(65)        # read up to ten bytes (timeout)
                #line = ser.readline()   # read a '\n' terminated line
                #b = ser.read_all()
                #c = ser.readall()
                #self._serial.in_waiting
                if self._data:
                    while (not self._did_read ) and (self._did_read != DEC.NOT_PROT) :
                        self.ver_serial()
                        #self._did_read = self._serial_protocol.read_Qr(self._data[:-2])
                        time.sleep(0.1)
                        self._data = self._data + self._serial.read(self._serial.in_waiting)

                    self._serial.reset_input_buffer()
                    self._serial.reset_output_buffer()

                    if self._did_read:
                        print (CONS.bcolors.OKGREEN+"--Serial Succesfully readed--")
                        print ("{}".format(self._data)+CONS.bcolors.ENDC)
                        
                        if self._data < 0 :
                            return False
                        else :
                            return self._data

                    elif self._did_read == DEC.NOT_PROT :
                        print (" NONE Serial Prot")
                        return False
                else :
                    return 0

        """
        except Exception as e:
            print (CONS.bcolors.FAIL+"Error Get Serial: {}".format(e)+CONS.bcolors.ENDC)            
            self._serial.reset_input_buffer()
            self._serial.reset_output_buffer()
            #logger.error('SERIAL_MODULE_ERROR THREAD_READING {}'.format(e))
            return False
        """
class USB_Serial():
    """
    This class Implement the serial communication in order to read a serial 
    QR camera through USB. 
    @param : port  Serial Port to connect with cammera (normal = /dev/ttyACM0) 
    @param : speed Serial Speed , normal Value 9600

    In order to read the data, calle the function : rec()
    """
    def __init__(self,port='/dev/ttyACM0',baudrate=9600):
        self.__connected= False
        self.__port = port
        self.__baudrate = baudrate
        
        try:
            self.__ser = serial.Serial(
            port= self.__port,
            baudrate = self.__baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1 )
            self.__connected = True
        except:
            self.__connected = False

    def __reconnecting(self):
        try:
            self.__ser = serial.Serial(
            port= self.__port,
            baudrate = self.__baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1 )
            self.__connected = True
        except:
            self.__connected = False
        finally:
            return self.__connected

    def test_serial(self):
        try:
            self.__serial_readable=self.__ser.readline()
            return True
        except:
            return self.__reconnecting()
        
    def qr_adq(self):
        if not self.__connected:
            return False
        try :
            while True:
                self.__serial_readable=ser.readline()
                if self.__serial_readable != b'':
                    return self.__serial_readable
                else :
                    print (self.__serial_readable)
        except :
            return False

################################

if __name__ == '__main__':
   
    # Test Just reading serial Port
    Serial_A = Just_Read()
    while True:
        leido = Serial_A.rec()
        print (leido)

#https://pyserial.readthedocs.io/en/latest/pyserial_api.html