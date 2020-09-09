#!/usr/bin/env python
# -*- coding: utf-8 -*-
_author_= "David Lizarazo"
_version_="1.0.0"

""" Crea y guarda en un archivo el numero del
 ID proccess, para poder ser eliminado 
 posteriormente mediante otro program 
 o desde el htop de alguna terminal """

import os
from time import ctime

def __get_PID():
   return (int(os.getpid()))

def __save_file(conca,data):
   print('*** Guardadno infomracion en archivo ***')
   log_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)),'log','pid_proc.txt')
   if conca:
      file = open(log_folder,'a+')
      file.write('{} ... {} \n'.format(data,ctime()))
      file.close()
   else: 
      file = open('log/pid_proc.txt','a+')
      file.write('{}... {} \n'.format(data,ctime()))
      file.close()

def save_PID():
    __save_file(True,__get_PID())

def ret_pid():
    return __get_PID()


