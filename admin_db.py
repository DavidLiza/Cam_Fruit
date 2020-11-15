#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__     = "David Lizarazo"


import os
import json
import datetime
from   time          import sleep

try: 
    import module.log               as log
    import module.constants         as CONS
    import module.databaseConsume   as SQL
except:
    import log
    import constants as CONS
    import sql_adq   as SQL

"""
This module is used to set the database information 
in order to make user cases , as if the device 
was or not setted before.
"""

def borrado():
    __action = """DELETE FROM data WHERE IDeye="{}" """.format(CONS.IDeye)
    __localdb = SQL.LocalDBConsumption(databasename= "location_info.db")
    __location_new = __localdb.consult(lite_consult=__action , modification=True)
    __localdb.close_connection()
    if __location_new :
        print ("Borrado Realizado")
        return True
    else:
        return False 

def no_conf ():
    print ("No Configurado Seleccionado")
    __action = """INSERT INTO data (IDeye,IDlocation,Lat,Lon,Tol,ssid,pswd,is_socket)
                    VALUES        ( "{}" ,""        ,0.0,0.0,0.0,NULL,NULL, {});""".format(CONS.IDeye,CONS.W_SOCKET)
    __localdb = SQL.LocalDBConsumption(databasename= "location_info.db")
    __location_new = __localdb.consult(lite_consult=__action , modification=True)
    __localdb.close_connection()
    if __location_new :
        print ("Clean Realizado")
        return True
    else:
        return False 

def config():
    print ("Configurado Seleccionado")
    __action = """INSERT INTO data (IDeye,IDlocation,Lat,Lon,Tol,ssid,pswd,is_socket)
                    VALUES        ( "{}" ,"Prueba"   ,4.72720929,-74.03403381,30,NULL,NULL, {});""".format(CONS.IDeye,CONS.W_SOCKET)
    __localdb = SQL.LocalDBConsumption(databasename= "location_info.db")
    __location_new = __localdb.consult(lite_consult=__action , modification=True)
    __localdb.close_connection()
    if __location_new :
        print ("Configurado Realizado")
        return True
    else:
        return False 

def select_contenedores():
    print ("SELECT Seleccionado")
    __action = """SELECT * FROM canastillas """
    __localdb = SQL.LocalDBConsumption(databasename= "contenedores.db")
    __location_new1 = __localdb.consult(lite_consult=__action , modification=False)
    
    __action = """SELECT * FROM estibas  """
    __localdb = SQL.LocalDBConsumption(databasename= "contenedores.db")
    __location_new2 = __localdb.consult(lite_consult=__action , modification=False)

    
    __action = """SELECT * FROM gatos """
    __localdb = SQL.LocalDBConsumption(databasename= "contenedores.db")
    __location_new3 = __localdb.consult(lite_consult=__action , modification=False)

    __localdb.close_connection()

    if __location_new1 or __location_new2 or __location_new3 :
        print (CONS.bcolors.CIAN+"*** Canastillas ***"+CONS.bcolors.ENDC)
        print (__location_new1)

        print (CONS.bcolors.CIAN+"*** Estibas ***"+CONS.bcolors.ENDC)
        print (__location_new2)

        print (CONS.bcolors.CIAN+"*** Gatos ***"+CONS.bcolors.ENDC)
        print (__location_new3)

        return True
    else:
        return False 

def pragma(table = "data", select_db="location_info.db" ):
    print ("Estructura DB seleccionada")
    __action = """PRAGMA TABLE_INFO({}) """.format(table)
    __localdb = SQL.LocalDBConsumption(databasename= select_db)
    __location_new = __localdb.consult(lite_consult=__action , modification=False)
    __localdb.close_connection()
    if __location_new :
        for fila in __location_new:
            print (fila)
        return True
    else:
        return False 


if __name__ == '__main__':
    repeating = True
    while repeating:
        print ("*** SELECCIONE EL CASO DE USUARIO A SIMULAR ***")
        print ("""1. Dispositivo Nuevo, DEFAULT. 
2. Dispositivo Nuevo, MAL Despachado/Configurado
3. Dispositivo Nuevo, Sin Configurar.
4. Dispositivo Configurado 
5. Select contenedores DB data
6. Pragma Tabla 
        """)
        
        caso = input (CONS.bcolors.OKBLUE+"Seleccion: "+CONS.bcolors.ENDC)
        
        try:
            if caso == str(1)  :
                if not borrado():
                    exit(0) 
            elif caso == str(2):
                mal_des()
            elif caso == str(3):
                no_conf()
            elif caso == str(4):
                config()
            elif caso == str(5):
                select_contenedores()
            elif caso == str(6):
                pragma(table="data" ,  select_db="location_info.db" )
            else :
                repeating = False
                print (CONS.bcolors.FAIL+"Seleccion incorrecta , saliendo "+CONS.bcolors.ENDC)
        finally:
            print (CONS.bcolors.CIAN+"Done")

        input ("Enter To Continue ..."+CONS.bcolors.ENDC)
        os.system('clear')
        