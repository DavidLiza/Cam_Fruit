#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__     = "David Lizarazo"
__copyright__  = "Copyright 2020, "
__credits__    = ["David Lizarazo"]
__version__    = "1.0.1"
__maintainer__ = "David Lizarazo"
__email__      = "davidlizarazovesga@hotmail.com"
__status__     = "Production"

import os
import sqlite3
import RPi.GPIO as GPIO
import urllib.request as url

try:
    import log
    import gpioModule as GPIOS
    import sql_adq    as SQL 
    import constants  as CONS
except:
    import module.log        as log
    import module.gpioModule as GPIOS
    import module.sql_adq    as SQL
    import module.constants  as CONS

logger = log.configure_logger('default')

class Initial_Configuration():
    """
    Class to check and set the initial configuration Device 
    @params  : NONE
    @returns : (int) The class returns the state of configuiration 
                To do so, create the constructor , and call the function 
                check_configuration. This Module can retorn a number from 0 to 5
                depending in the state of the configuration:
    - 0 - Device coudnt be configured (Denied Permition or missing data)
    - 1 - Device configured correctly
    - 2 - 
    - 3 - Device configured with Socket and NO Internet connection(Captor)
    - 5 - StandBy device (Waiting For modifications)
    """
    def __init__(self):
        print (CONS.bcolors.HEADER+"Initial Configuration"+CONS.bcolors.ENDC)
        try :
            self.__localdb = SQL.LocalDBConsumption(databasename= "location_info.db")
            self.__location_info    = self.__localdb.consult("SELECT * FROM data")
            self.__location_struct  = self.__localdb.consult("PRAGMA TABLE_INFO(data)")
            self.__localdb.close_connection()

        except :
            logger.error('OJE009, LAB')

    def check_configuration(self):
        
        self.__ideye = CONS.IDeye
        if not self.__ideye:
            return 0

        # Primera vez que se enciende el dispositivo
        if not self.__location_info :
            return self.__first_boot()
        else:
            self.__yeap={}
            counter = 0
            for col_name in self.__location_struct:
                self.__yeap["{}".format(col_name[1])] = self.__location_info[0][counter]
                counter = counter+1

        #Base de datos iniciada , pero sin modificarse
        if self.__location_info[0][1] == '' or ( self.__location_info[0][2] == 0 and self.__location_new[0][3] == 0 )  :
            print ('Sin modificaciones ,Lea codigo , configure!') 
            return 5
        if self.__location_info[0][7] == None or self.__location_info[0][7] == 0 :    
            return 1

        return 0

    def __first_boot (self):
       try:
            _action = """INSERT INTO data (IDeye,IDlocation,Lat,Lon,Tol,ssid,pswd,is_socket)
                         VALUES           ( "{}" ,""        ,0.0,0.0,0.0,NULL,NULL, {});""".format(CONS.IDeye,CONS.W_SOCKET)
            self.__localdb = SQL.LocalDBConsumption(databasename= "location_info.db")
            self.__location_new = self.__localdb.consult(lite_consult=_action , modification=True)
            self.__location_info = self.__localdb.consult("SELECT * FROM data")
            self.__localdb.close_connection()
            
            if self.__location_new  :
                print (CONS.bcolors.WARNING+'Primer acceso , lea el siguiente Codigo en pantalla!'+CONS.bcolors.ENDC) 
                return 5
            else :  return 0
                
       except:
            print ("Error First Boot")
            logger.eror('OJE009 FB_DB')
            return 0

    # Used for main.py , to get the last location info
    def get_location_info(self):
        return self.__location_info[0][1],self.__location_info[0][2],self.__location_info[0][3], self.__location_info[0][10]


if __name__ == '__main__':
    """
    This will be run when the program is call
    and will test the main class (Initial_Config)
    even create a sentence in DB in case it didnt 
    exist
    """

    init = Initial_Configuration()
    state_configuration = init.check_configuration()
    print (CONS.bcolors.WARNING+'State {}'.format(state_configuration)+CONS.bcolors.ENDC)
    data_info = init.get_location_info()
    print (CONS.bcolors.HEADER+'Location Info {}'.format(data_info)+CONS.bcolors.ENDC)