import sys
import pygame
import pygame.camera

pygame.init()
pygame.camera.init()
cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0],(32,24))
cam.start()

image1 = cam.get_image()
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
