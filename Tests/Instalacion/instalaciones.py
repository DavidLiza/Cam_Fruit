#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_author_= "David Lizarazo"
_version_="1.0.0"

import os
import sys

py_version = sys.version_info[0]
if py_version != 3 :
   print ("No esta corriendo python3")
   sys.exit()
else : 
   print ("Corriendo Python3")

input ("Holi")
#***** Actualizar y Mejorar sin preguntar *****
try:
   os.system('sudo apt-get update')
except:
   print('Couldnt do the update')

try:
   os.system('sudo apt-get upgrade')
except:
   print('Couldnt do the upgrade')

#****** pip3  ******
try:
  entrada = input ("Desea visualziar todos los elementos de pip3 : (y/n)")
  if entrada == 'y':
    os.system('pip3 freeze')
  else:
    os.system('pip3 --version')
except:
   os.system('sudo apt-get -y install python3-pip')
   os.system('pip3 --version')


#***** Sqlite3 *****
entrada = input ("Desea instalar (sqlite3) : (y/n)")
if entrada == 'y':
  try:
     import sqlite3
     print ("****** sqlite3 LIBRERIA YA INSTALADA ********")
  except:
     os.system('sudo apt-get install sqlite3')

#**** YAML *******
entrada = input ("Desea instalar (YAML) : (y/n)")
if entrada == 'y':
  try:
     import yaml
  except:
     os.system('sudo pip3 install pyyaml')

#****** RPI ******
entrada = input ("Desea instalar (RPI) : (y/n)")
if entrada == 'y':
  try:
     import RPi.GPIO as GPIO
  except:
     os.system('sudo pip3 --version')

#****** Cython ******
entrada = input ("Desea instalar (sqlite3) : (y/n)")
if entrada == 'y':
  try:
     import Cython
  except:
     os.system('sudo pip3 install Cython')

#****** Barcode ******
entrada = input ("Desea instalar (barcode) : (y/n)")
if entrada == 'y':
  try:
     import barcode
  except:
     os.system('sudo pip3 install python-barcode')


#****** Pygame ******
entrada = input ("Desea instalar (Pygame) : (y/n)")
if entrada == 'y':
  try:
     import pygame
  except:
     os.system('sudo pip3 install pygame')


#****** Requests ******
entrada = input ("Desea instalar (requests) : (y/n)")
if entrada == 'y':
  try:
     import requests
  except:
     os.system('sudo pip3 install requests')

#****** Tkinter ******
entrada = input ("Desea instalar (requests) : (y/n)")
if entrada == 'y':
  try:
     import requests
  except:
     os.system('sudo pip3 install tkinter')



#******* pyzbar ********
"""
entrada = input ("Desea instalar (sqlite3) : (y/n)")
if entrada == 'y':
  try:
     import pyzbar
  except:
     os.system('sudo pip3 install pyzbar')
"""

