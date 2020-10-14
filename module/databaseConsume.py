#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_author_ = 'David Lizarazo'
_version_ = '1.0.0'

import sqlite3
import log

logger = log.configure_logger('default')

class DataBaseConsumption():

    def __init__(self,databasename='Module/kike',table_consult="Authorized",Data="IDowner"):
        self.__dbname =databasename + '.db'
        self.__dbtable=table_consult
        self.__dbdata =Data

    def __get_data(self):
        try:
            sqliteConnection = sqlite3.connect(self.__dbname)
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_select_query = """SELECT """+ self.__dbdata + """ from """ + self.__dbtable
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            
            cursor.close()
            return records

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed")

    def __get_entrance(self):
        try:
            sqliteConnection = sqlite3.connect(self.__dbname)
            cursor = sqliteConnection.cursor()
            
            if self.__seaTab :
                sqlite_select_query = """SELECT Name1,IDowner FROM Authorized where AuthorizedId=?""" 
                cursor.execute(sqlite_select_query,(self.__Idscan,))
                records = cursor.fetchall()
                cursor.close()
                return records 
            else:
                sqlite_select_query = """SELECT Name1,Lastname1 FROM Owner where IDowner=?""" 
                cursor.execute(sqlite_select_query,(self.__Idscan,))
                records = cursor.fetchall()
                cursor.close()
                return records 


        except sqlite3.Error as error:
            logger.info('Failed to read data from sqlite table :**** {}'.format(error))
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed")


    def get_info(self,table_consult="Authorized",Data="IDowner"):
        self.__dbtable=table_consult
        self.__dbdata =Data
        return self.__get_data()

    def get_entrance(self,IdScanned=1019128590,Authorized=True):
        self.__Idscan =IdScanned
        self.__seaTab = Authorized 
        return self.__get_entrance()

def main():
   Base_de_datos=DataBaseConsumption(databasename='kike')
   #Name= Base_de_datos.get_info(table_consult="Authorized",Data="Name1")
   #print(Name)
   real=Base_de_datos.get_entrance(IdScanned=80086625,Authorized=False)
   print(real)
   if not real:
     print ("Vaciooo")


if __name__ == '__main__':
    print('Started as Main')
    main()

