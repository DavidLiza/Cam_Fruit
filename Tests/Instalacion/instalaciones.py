#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_author_= "David Lizarazo"
_version_="1.0.0"

import os

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

#******* pyzbar ********
"""
entrada = input ("Desea instalar (sqlite3) : (y/n)")
if entrada == 'y':
  try:
     import pyzbar
  except:
     os.system('sudo pip3 install pyzbar')
"""

#***** MYSQL ******
"""
entrada = input ("Desea instalar (sqlite3) : (y/n)")
if entrada == 'y':
  try: 
     import mysql.connector
  except:
     os.system('sudo pip3 install mysql-connector')
"""

#****** espeak ******
entrada = input ("Desea instalar (modulo espeak) : (y/n)")
if entrada == 'y':
  try:
      os.system('sudo apt-get install espeak')
  except:
      print ("Couldnt Install Espeak")

#****** mpg123 ******
print ("(mpg123 : reproductor audio) , este ese necesario para reproduccion de gTTS")
entrada = input (" Desea instalar  : (y/n)")
if entrada == 'y':
  try:
      os.system('sudo apt-get -y install mpg123')
  except:
      print ("Couldnt Install mpg123")

#****** gtts ****** reproductor de audio ( Google Text to speech)
entrada = input ("Desea instalar (modulo espeak) : (y/n)")
if entrada == 'y':
  try:
     from gtts import gTTS
  except:
     os.system('sudo pip3 install gTTS')


#****** rpi_rf_module ******
entrada = input ("Desea instalar (modulo espeak) : (y/n)")
if entrada == 'y':
  try:
      os.system('sudo pip3 rpi_rf')
  except:
      print ("Couldnt install RF module")

#****** MP4 converter *************
entrada = input ("Desea instalar (Conversor a MP4) : (y/n)")
if entrada == 'y':
  try:
      os.system('sudo apt install -y gpac')
  except:
      print ('Couldnt Install MP4 converter')

# ***** Instalacion de Open CV ******* 
print ("Desea instalar opencv de una ?? (y/n)")
print ("Usted debe encontrarse en home")

opcv = input()

if opcv == 'y' :
  print ('Usted dijo que si ')
  os.system('chmod +x *.sh')
  os.system('./download-opencv.sh')
  os.system('./install-deps.sh')
  os.system('./build-opencv.sh')
  os.system('chmod +x *.sh')
  print('Ingrese en de la siguiente manera y ejecute el comando mostrado :')
  print ('cd ~/opencv/opencv-4.1.2/build')
  print ('sudo make install')


else : 
 print ('Open Cv no sera instalado !! ')

