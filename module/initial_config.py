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
import urllib.request as url

try:
    import log
    import databaseConsume          as SQL 
    import constants                as CONS
except:
    import module.log               as log
    import module.databaseConsume   as SQL
    import module.constants         as CONS

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
    - 1 - Device with data in DB
    - 2 - No wifi DATA
    - 3 - No Contenedors DATA

    - 5 - StandBy device (Waiting For modifications)
    """
    def __init__(self):
        print (CONS.bcolors.HEADER+"Initial Configuration"+CONS.bcolors.ENDC)
        self.get_wifi_data()
        self.get_canas_data()
        self.get_pall_data()

    def check_configuration(self):
        
        if not CONS.IDevice: return 0

        # Primera vez que se enciende el dispositivo
        if not self.__devicen_info :                        return 2
        elif not self.__canastillas or not self.__pallets:  return 3
        else:
            return 1

    def get_wifi_data (self ,   org = False):
        try:
            self.__devicedb = SQL.LocalDBConsumption(databasename= "device.db")
            self.__devicen_info   = self.__devicedb.consult("SELECT * FROM wifis")
            self.__device_struct  = self.__devicedb.consult("PRAGMA TABLE_INFO(datwifisa)")
            self.__devicedb.close_connection()
            if org:
                __myjson={}
                counter = 0
                for col_name in self.__device_struct:
                    __myjson["{}".format(col_name[1])] = self.__devicen_info[0][counter]
                    counter = counter+1
                return __myjson


        except :
            print (CONS.bcolors.FAIL+"FAILED TO GET DB"+CONS.bcolors.ENDC)
            logger.error('get_db Error')


    def get_canas_data (self ,  org = False):
        try:
            self.__contedb = SQL.LocalDBConsumption(databasename= "contenedores.db")
            self.__canastillas   = self.__contedb.consult("SELECT * FROM canastillas")
            self.__cont_Struct   = self.__devicedb.consult("PRAGMA TABLE_INFO(canastillas)")
            self.__contedb.close_connection()
            if org:
                __myjson={}
                counter = 0
                for col_name in self.__cont_Struct:
                    __myjson["{}".format(col_name[1])] = self.__canastillas[0][counter]
                    counter = counter+1
                return __myjson

        except :
            print (CONS.bcolors.FAIL+"FAILED TO GET DB"+CONS.bcolors.ENDC)
            logger.error('get_db Error')


    def get_pall_data (self ,   org = False):
        try:
            self.__contedb = SQL.LocalDBConsumption(databasename= "contenedores.db")
            self.__pallets   = self.__contedb.consult("SELECT * FROM estibas")
            self.__cont_Struct   = self.__devicedb.consult("PRAGMA TABLE_INFO(estibas)")
            self.__contedb.close_connection()
            if org:
                __myjson={}
                counter = 0
                for col_name in self.__cont_Struct:
                    __myjson["{}".format(col_name[1])] = self.__pallets[0][counter]
                    counter = counter+1
                return __myjson

        except :
            print (CONS.bcolors.FAIL+"FAILED TO GET DB"+CONS.bcolors.ENDC)
            logger.error('get_db Error')



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
    
    data_info = init.get_canas_data()
    print (CONS.bcolors.HEADER+'Canastillas Info {}'.format(data_info)+CONS.bcolors.ENDC)
    data_info = init.get_pall_data()
    print (CONS.bcolors.HEADER+'Palletes Info {}'.format(data_info)+CONS.bcolors.ENDC)