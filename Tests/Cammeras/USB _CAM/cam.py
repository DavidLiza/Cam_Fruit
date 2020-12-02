# -*- coding: utf-8 -*-
__author__ = "David Lizarazo"
__version__ = "1.0.0"

# Este modulo captura imagen de una camara conectada por USB
import sys
import pygame
import pygame.camera
from io import StringIO
from PIL import Image
from io import BytesIO


# -- Vars Init --
img_size = (640,480)
pygame.camera.init()
cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0],img_size)
cam.start()


# -- Conversion a Binario --
image_normal = cam.get_image()
data = pygame.image.tostring(image_normal, 'RGBA')
img = Image.frombytes('RGBA',img_size, data)
buffer = BytesIO()
img.save(buffer,'png')
vari_png =  (buffer.getvalue())
print (vari_png)


# -- Raw Image data --
image1 = cam.get_raw()
img = Image.frombytes(mode="P", size=img_size, data=image1 ) # , decoder_name="raw" , 'F;16'
print (img)
print (list(img.getdata()))


zdata = StringIO()
zdata = cam.get_raw()
print (zdata)

pygame.image.save(image1,'101.png')
cam.stop()

"""
while True:
   image1 = cam.get_image()
   image1 = pygame.transform.scale(image1,(640,480))

   for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cam.stop()
            pygame.quit()
            sys.exit()

import pygame, sys
from pygame.locals import *
import pygame.camera
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(352,288))
cam.start()
image= cam.get_image()
pygame.image.save(image,'101.bmp')
cam.stop()
"""
