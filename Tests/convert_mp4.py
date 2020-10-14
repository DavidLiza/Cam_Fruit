#!/usr/bin/env python
#-*- coding: utf-8 -*-
_author_= "David Lizarazo"
_version_="1.0.0"

import os
from subprocess import call

"""
# Ambas funcionan
print ("Proceso hecho con ...os... ")
os.system("ls -l")
print ("Proceso hecho con ...call...")
call(["ls","-l"])
"""

os.system ('MP4Box -add video.h264 video.mp4')
os.system ('rm video.h264')

# Infomration from :
# https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspivid.md

