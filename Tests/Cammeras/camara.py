from picamera import PiCamera
from time import sleep

camera = PiCamera()
print("***Camera information***")
print("Resolution: {}".format(camera.resolution))
print("Framerate : {}".format(camera.framerate))
print("Rotation  : {}".format(camera.rotation))
print("Zoom      : {}".format(camera.zoom))
print("WAIT ...")
#_get_camera_settings()
camera.rotation=180
print("Rotation  : {}".format(camera.rotation))
sleep(2)
camera.capture('FOO.jpg')
camera.start_recording('/home/pi/Desktop/video.h264')
sleep(10)
camera.stop_recording()


#https://picamera.readthedocs.io/en/release-1.10/api.html
# vcgencmd get_camera