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

    def __init__(self,speed = 9600 , port = 'ttyAMA0' , configure = False):
        self.__speed = speed
        self.__port  = '/dev/'+ port
        self.__isRun = False
        self.__wdec   = True
        self.__configure = True if configure ==5 else False 
        try:
            self._serial   = serial.Serial(self.__port, self.__speed )
            self.__isRun = True
        except Exception as e:
            logger.info('OJE008 INIT_CONNECTION ')
            self.__isRun = False
            self._serial = False

        self._serial_protocol = DEC.Qr_Protocol()

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
        
    def set_configure(self,configure):
        self.__configure = configure 
        self._serial_protocol.set_key(newkey=self.__newkey)

    def get_decoded(self,data_protocol):
        to_return= self._serial_protocol.get_Qr_Data(data_protocol[:-2])
        if not to_return:
            self.__configure = 5 if self.__configure != 5 else 1
            self.set_configure(configure=self.__configure)
            to_return= self._serial_protocol.get_Qr_Data(data_protocol[:-2])
            return to_return
        else:
            return to_return
    
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
        
        self._did_read = True
        
        try:
            while self.__isRun:
                    self._data=self._serial.read(self._serial.in_waiting)
                    if self._data:
                        while (self._did_read ) and (self._did_read != DEC.NOT_QR_PROT) :
                            self._did_read = self._serial_protocol.read_Qr(self._data[:-2])
                            time.sleep(0.1)
                            self._data = self._data + self._serial.read(self._serial.in_waiting)

                        self._serial.reset_input_buffer()
                        self._serial.reset_output_buffer()

                        if not self._did_read:
                            print (CONS.bcolors.OKGREEN+"--Protocolo Succesfully readed--"+CONS.bcolors.ENDC)
                            return self._data

                        elif self._did_read == DEC.NOT_QR_PROT :
                            print ("QR with NONE Protocol")
                            logger.error('SERIAL_MODULE_INFO NO_PROTOCOL')
                            logger.error('{}'.format(self._data))
                            return False

        except Exception as e:
            print ("Error Camara Serial: {}".format(e))            
            self._serial.reset_input_buffer()
            self._serial.reset_output_buffer()
            logger.error('SERIAL_MODULE_ERROR THREAD_READING {}'.format(e))
            return False

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
   
    while True:
        # Test Just reading serial Port
        Serial_A = Just_Read()
        leido = Serial_A.rec()
        print (Serial_A.get_decoded(leido))

#https://pyserial.readthedocs.io/en/latest/pyserial_api.html