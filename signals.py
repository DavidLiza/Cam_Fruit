# -*- coding: utf-8 -*-
__author__     = "David Lizarazo"
__copyright__  = "Copyright 2020"
__credits__    = ["David Lizarazo"]
__version__    = "1.0.0"
__maintainer__ = "David Lizarazo"
__email__      = "davidlizarazovesga@hotmail.com"
__status__     = "Desarrollo"

from blinker import signal


Sounds         = signal ('conf/play GPIO')
Start_Config   = signal ('Configuring_camara')
Camara_frame   = signal ('Capturing_video')
Decoding       = signal ('Information_decoding')
Scanning       = signal ('Ultrasonic_Proccess')

