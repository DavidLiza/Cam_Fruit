#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_author_= "David Lizarazo"
_version_="1.0.0"

import os
import sys

# Colores para impresion 
class bcolors:
    #Colors
    HEADER = '\033[95m'  # MAGENTA
    OKBLUE = '\033[94m'  # BLUE
    OKGREEN = '\033[92m' # GREEN
    WARNING = '\033[93m' # YELLOW
    FAIL = '\033[91m'    # RED
    CIAN = '\033[96m'    # CIAN
    
    #Instructions
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


py_version = sys.version_info[0]
if py_version != 3 :
   print (bcolors.FAIL+"No esta corriendo python3"+bcolors.ENDC)
   sys.exit()
else : 
   print ("Corriendo Python3")

#***** Actualizar y Mejorar sin preguntar *****
try:
   os.system('sudo apt-get update')
except:
   print('Couldnt do the update')

try:
   os.system('sudo apt-get upgrade')
except:
   print(bcolors.FAIL+'Couldnt do the upgrade'+bcolors.ENDC)

#****** pip3  ******
try:
  entrada = input (bcolors.HEADER+"Desea visualziar todos los elementos de pip3 : (y/n)"+bcolors.ENDC)
  if entrada == 'y':
    os.system('pip3 freeze')
  else:
    os.system('pip3 --version')
except:
   os.system('sudo apt-get -y install python3-pip')
   os.system('pip3 --version')


#***** Sqlite3 *****
entrada = input (bcolors.HEADER+"Desea instalar (sqlite3) : (y/n)"+bcolors.ENDC)
if entrada == 'y':
     os.system('sudo pip install pyarmor')
     os.system('sudo pip3 install pyarmor')
     
     
#***** Pyarmor *****
entrada = input (bcolors.HEADER+"Desea instalar (pyarmor) : (y/n)"+bcolors.ENDC)
if entrada == 'y':
  try:
     import sqlite3
     print ("****** Pyarmor LIBRERIA YA INSTALADA ********")
  except:
     os.system('sudo apt-get install sqlite3')
    


#***** VNC *****
entrada = input (bcolors.HEADER+"Desea instalar (VNC) : (y/n)"+bcolors.ENDC)
if entrada == 'y':
     os.system('sudo apt install realvnc-vnc-server realvnc-vnc-viewer')


#**** YAML *******
entrada = input (bcolors.HEADER+"Desea instalar (YAML) : (y/n)"+bcolors.ENDC)
if entrada == 'y':
  try:
     import yaml
  except:
     os.system('sudo pip3 install pyyaml')

#****** RPI ******
entrada = input (bcolors.HEADER+"Desea instalar (RPI) : (y/n)"+bcolors.ENDC)
if entrada == 'y':
  try:
     import RPi.GPIO as GPIO
  except:
     os.system('sudo pip3 --version')

#****** Cython ******
entrada = input (bcolors.HEADER+"Desea instalar (sqlite3) : (y/n)"+bcolors.ENDC)
if entrada == 'y':
  try:
     import Cython
  except:
     os.system('sudo pip3 install Cython')

#****** Barcode ******
entrada = input (bcolors.HEADER+"Desea instalar (barcode) : (y/n)"+bcolors.ENDC)
if entrada == 'y':
  try:
     import barcode
  except:
     os.system('sudo pip3 install python-barcode')


#****** Pygame ******
entrada = input (bcolors.HEADER+"Desea instalar (Pygame) : (y/n)"+bcolors.ENDC)
if entrada == 'y':
  try:
     import pygame
  except:
     os.system('sudo pip3 install pygame')


#****** Requests ******
entrada = input (bcolors.HEADER+"Desea instalar (requests) : (y/n)"+bcolors.ENDC)
if entrada == 'y':
  try:
     import requests
  except:
     os.system('sudo pip3 install requests')

#****** Tkinter ******
entrada = input (bcolors.HEADER+"Desea instalar (tkinter) : (y/n)"+bcolors.ENDC)
if entrada == 'y':
  try:
     import tkinter
  except:
      os.system('sudo pip3 install tkinter')
      os.system('sudo apt-get install python3-pil python3-pil.imagetk')

#******* pyzbar ********
"""
entrada = input ("Desea instalar (sqlite3) : (y/n)")
if entrada == 'y':
  try:
     import pyzbar
  except:
     os.system('sudo pip3 install pyzbar')
"""

