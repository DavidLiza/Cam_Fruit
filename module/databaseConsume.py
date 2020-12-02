#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__     = "David Lizarazo"
__copyright__  = "Copyright 2019, Ojo Biometrico"
__credits__    = ["David Lizarazo"]
__license__    = "GPL"
__version__    = "1.0.0"
__maintainer__ = "David Lizarazo"
__email__      = "dlizarazo@identica-sa.com"
__status__     = "Production"

import sqlite3				# To consult the local DataBases
import os
import json
import datetime

try: 
    import module.constants as CONS
except:
    import constants as CONS

dir_path = os.path.dirname(os.path.realpath(__file__))
if dir_path[len(dir_path)-6 : len(dir_path)] == 'module':
    foldercontainer=dir_path+str("/../database/")
else:
    foldercontainer=dir_path+str("/database/")

class LocalDBConsumption():
    """
    Class LocalDBConsumption, to manage infomration 
    from local database. This also contain predefined 
    functions to aquiere entrance from a person. 

    To make a simple consult call this class with the 
    parameter database name and then 
    the function consult.

    @params : databasename (string) Database to consult in
                           This Database must be in a previous folder 
                           called ../dbs/

    @returns Dont return, but call the parameter .__isconnected

    """
    def __init__(self,databasename='location_info.db'):
        self.__dbname = foldercontainer + databasename
        if self.__dbname[len(self.__dbname)-3 : len(self.__dbname)] != '.db':
            self.__dbname = self.__dbname + '.db'

        try:
            self.__sqliteConnection = sqlite3.connect(self.__dbname)
            self.__cursor      = self.__sqliteConnection.cursor()
            self.__isconnected = True
        except sqlite3.Error as error:
            print("Failed to connect to sqlite ", error)
            #logger.error('OJE006')
            self.__isconnected = False

    def consult(self , lite_consult , modification = False):
        """
        Function to make a simple consult in the database defined 
        in the class call. The consult can just get data or set.
        @params  : lite_consult
        @params  : modification
        @returns : [boolean, str] , in case was a SELECT consult, 
                   the function returns the data asked for 
                   In case modification need to be done. Th function 
                   return True if the procces was done succesfully
        """
        self.__consult = lite_consult
        try :
            if self.__isconnected:
                self.__cursor.execute(self.__consult)
                if modification:
                   self.__response = self.__cursor.fetchall()
                   self.__sqliteConnection.commit()
                   #print (self.__response)
                   return True
                self.__response = self.__cursor.fetchall()
                # print (self.__response)
                return self.__response

        except Exception as e:
             print ('Error in consult : {}'.format(e))
             #logger.error('OJE006 Consult')
             return False

    def close_connection (self):
       try :
           if self.__isconnected:
               self.__cursor.close()
               self.__sqliteConnection.close()
               self.__isconnected = False
       except Exception as e :
           pass
           # logger.error('OJE006 Closing DB')
       finally :
           if self.__isconnected:
               self.__sqliteConnection.close()
               print("Second try closed")

 
    def __get_entrance(self):
       try:
           self.__sqlite_select_query = """SELECT Name FROM Owner where IDowner=?"""
           self.__cursor.execute(self.__sqlite_select_query,(self.__Idscan,)) # La (,) es necesaria
           self.__records = self.__cursor.fetchall()
           self.close_connection()
           if not self.__records:
              return False
           else:
              return True
       except Exception as e :
           pass
           #print ("Error in get entrance SQLITE3 database :  {}".format(e))
           #logger.error('OJE006 Entrance')


    def __login_user(self):
       try: # Si no es nulo y es igual al almacenado
           self.__sqlite_select_query = """SELECT Name , Lastname FROM Owner 
           where IDowner={} and Pswd ='{}' and SecLevel ='admin' """.format(self.__id_login,str(self.__pass_login))
           #print (self.__sqlite_select_query)
           self.__cursor.execute(self.__sqlite_select_query) # La (,) es necesaria
           self.__records = self.__cursor.fetchall()
           self.close_connection()
           if not self.__records:
                return False
           else:
                self.__jsonlogin = {
                    "name":     self.__records[0][0],
                    "lastname": self.__records[0][1],
                    "idowner"  : self.__id_login
                }
                return True
       except Exception as e :
           print ("Error in __login_user SQLITE database {}".format(e))
           #logger.error('OJE006 LOGIN')
          
    def is_token_activated (self,token,idown):
        """
        Check wheter the token is still enable or if 
        has transcur more than 30 minutes
        @params : token, Token given by WEPPAGE, to compare with DB 
        @params : idown, Identification Number for compare with the Token
        """
        try: # Si no es nulo y es igual al almacenado
            self.__token = token
            self.__query = """SELECT Name FROM Owner 
            where IDowner={} and Token ='{}' and SecLevel ='admin' """.format(idown,token)
            self.__cursor.execute(self.__query) # La (,) es necesaria
            self.__records = self.__cursor.fetchall()
            self.close_connection()
            if not self.__records:
                return False
            else:
                return True
        except Exception as e :
            print ("Error in is_token_activated SQLITE3 database: {}".format(e))
            #logger.error('OJE006 TOKEN')

    def get_entrance(self,IdScanned=1019128590): 
        """
        Decide if a User have permitions or not
        @params  : (int) IdScanned, Identification Number 
        @returns : (Bool) If allowed, returns True
        """
        self.__Idscan =IdScanned
        return self.__get_entrance()
       
    def login_user(self,IdUser=674178 , PasUser= "admin"): 
        """
        Used to validate information given by the configuration 
        proccess. Checking in local DB , wheter The User or 
        passwords are correct. And the times tried to login. 
        @params  : (int) IdUser, Identification Number 
        @params  : (string) PasUser, Encrypted password to compare with 
                    db password pre saved
        @returns : If login was succesfully, returns  json structure 
                  with name,lastname, and idowner from user, or None if not
        """
        self.__id_login   = IdUser
        self.__pass_login = PasUser
       
        if self.__pass_login != None :
            self.__login_user()
            return self.__jsonlogin
        return None
     
######## Test Y Main ############
def test_newlite ():
   db_sql = LocalDBConsumption(databasename='location_info.db')
   resultado = db_sql.consult(lite_consult = "SELECT IDlocation FROM data WHERE IDeye=1234;")
   db_sql.close_connection()
   print (resultado)

   db_sql = LocalDBConsumption(databasename='eye_access.db')
   resultado = db_sql.consult(lite_consult = "SELECT * FROM Owner;")
   db_sql.close_connection()
   print (resultado)

if __name__ == '__main__':
    import constants as CONS		
    print('Started as Main')
    test_newlite()
    
