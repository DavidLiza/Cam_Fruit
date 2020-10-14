import os
import time
import digitalio
import board
from PIL import Image, ImageOps
import adafruit_rgb_display.ili9341 as ili9341


class Frame:
    def __init__(self, duration=0):
        self.duration = duration
        self.image = None

class AnimatedGif:
    def __init__(self, display, width=None, height=None, folder=None):
        self._frame_count = 0
        self._loop = 0
        self._index = 0
        self._duration = 0
        self._gif_files = []
        self._frames = []
 
        if width is not None:
            self._width = width
        else:
            self._width = display.width
        if height is not None:
            self._height = height
        else:
            self._height = display.height
        self.display = display
        
        if folder is not None:
            self.load_files(folder)
            self.run()
            
    def advance(self):
        self._index = (self._index + 1) % len(self._gif_files)
     
    def back(self):
        self._index = (self._index - 1 + len(self._gif_files))  % len(self._gif_files)

    def load_files(self, folder):
        gif_files = [f for f in os.listdir(folder) if f.endswith('.gif')]
        for gif_file in gif_files:
            gif_file=folder+"/"+gif_file
            image = Image.open(gif_file)
            if image.is_animated:
                self._gif_files.append(gif_file)

        if not self._gif_files:
            print("No Gif files found in current folder")
            exit()
            
    def preload(self):
        image = Image.open(self._gif_files[self._index])
        print("Loading {}...".format(self._gif_files[self._index]))
        if "duration" in image.info:
            self._duration = image.info["duration"]
        else:
            self._duration = 0
        if "loop" in image.info:
            self._loop = image.info["loop"]
        else:
            self._loop = 1
        self._frame_count = image.n_frames
        print ("Loop {}".format(self._loop))
        print ("Frame count {}".format(self._frame_count))
        self._frames.clear()
        print ("Frame count {}".format(self._frame_count))
        
        for frame in range(self._frame_count):
            image.seek(frame)
            # Create blank image for drawing.
            # Make sure to create image with mode 'RGB' for full color.
            frame_object = Frame(duration=self._duration)
            if "duration" in image.info:
                frame_object.duration = image.info["duration"]
            frame_object.image = ImageOps.pad(  # pylint: disable=no-member
                image.convert("RGB"),
                (self._width, self._height),
                method=Image.NEAREST,
                color=(0, 0, 0),
                centering=(0.5, 0.5),
            )
            self._frames.append(frame_object)

    def play(self):
        self.preload()
 
        # Check if we have loaded any files first
        if not self._gif_files:
            print("There are no Gif Images to Play")
            return False
        while True:
            for frame_object in self._frames:
                start_time = time.monotonic()
                self.display.image(frame_object.image)
                """
                if not self.advance_button.value:
                    self.advance()
                    return False
                if not self.back_button.value:
                    self.back()
                    return False
                """
                while time.monotonic() < (start_time + frame_object.duration / 1000):
                    pass
 
            if self._loop == 1:
                return True
            if self._loop > 0:
                self._loop -= 1
                
    def run(self):
        while True:
            auto_advance = self.play()
            if auto_advance:
                self.advance()      


cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D24)
reset_pin = digitalio.DigitalInOut(board.D25)
# Config for display baudrate (default max is 64mhz):
BAUDRATE = 64000000
# Setup SPI bus using hardware SPI:
spi = board.SPI()
# Create the display:
disp = ili9341.ILI9341(spi,rotation=90,cs=cs_pin,dc=dc_pin,rst=reset_pin,baudrate=BAUDRATE,) # 2.2", 2.4", 2.8", 3.2" ILI9341

if disp.rotation % 180 == 90:
    disp_height = disp.width  # we swap height/width to rotate it to landscape!
    disp_width = disp.height
else:
    disp_width = disp.width
    disp_height = disp.height

dirpath = os.getcwd()
dirpath = dirpath+"/GIFS"
print("current directory is : " + dirpath)


gif_player = AnimatedGif(disp, width=disp_width, height=disp_height, folder=dirpath) #"."

# Tutorial 
# https://learn.adafruit.com/pitft-linux-python-animated-gif-player/python-setup-2

# URL , Para descargar GIFs
# https://giphy.com/


# Dependencias del codigo 
# sudo pip3 install adafruit-circuitpython-rgb-display
# sudo apt-get install ttf-dejavu
# sudo apt-get install python3-pil
# sudo apt-get install python3-numpy


