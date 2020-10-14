# -*- coding: utf-8 -*-
__author__     = "David Lizarazo"
__copyright__  = "Copyright 2019, Ojo Biometrico"
__credits__    = ["Sebastian Estupiñan, David Lizarazo"]
__license__    = "GPL"
__version__    = "1.0.0"
__maintainer__ = "David Lizarazo"
__email__      = "sestupinan@identica-sa.com"
__status__     = "Production"

from blinker import signal

CamError       = signal ('camera-not-detected')
Sounds         = signal ('conf/play GPIO')
Start_Config   = signal ('Configuring_camara')
Camara_frame   = signal ('Capturing_video')
Decoding       = signal ('Information_decoding')
Second_Cam     = signal ('Second_Cam_function')
Authentication = signal ('Authentication_Process')

