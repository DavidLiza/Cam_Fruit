#!/usr/bin/env python
#-*- coding: utf-8 -*-
_author_= "David Lizarazo"
_version_="1.0.0"

import urllib.request as url
#import Module.
#import log

#__logger = log.configure_logger('default')
def basic_connected ():
    try:
        url.urlopen("http://google.com")
    except urllib2.URLError as e:
        print( "Network currently down." )
        return 0
    else:
        print( "Up and running." )
        return 1

def config_connection():
    loop_value = True
    announced  = False
    while loop_value :
        try:
            url.urlopen("http://google.com")
        except urllib2.URLError as e:
            print( "Network currently down." )
        else:
            print( "Up and running." )
            announced = False
            loop_value = False
        if not announced:
            if loop_value:
                print ("Espeak :No se ha podido conectar a internet. Conecte el cable de red  y no lo desconecte hasta terminar el proceso de configuracion ")
            else:
                print ("Espeak :Conectado satisfactoriamente , espere hasta que el proceso de configuracion termine ")
            announced = True

if __name__ == '__main__':
    basic_connected()
    config_connection()
