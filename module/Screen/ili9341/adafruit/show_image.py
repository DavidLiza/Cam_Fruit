

import digitalio
import board
from PIL  import Image, ImageDraw
from time import sleep
import adafruit_rgb_display.ili9341 as ili9341


def show_image(device,imageToShow):
    # we swap height/width to rotate it to landscape!
    if device.rotation % 180 == 90:
        height = device.width  
        width = device.height
    else:
        width = device.width  
        height = device.height
        
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)
    
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    device.image(image)
    
    # Scale the image to the smaller screen dimension
    image_ratio = imageToShow.width / imageToShow.height
    screen_ratio = width / height
    #print ("Image Ratio : {} \nScreen Ratio {}".format(image_ratio,screen_ratio))
    if screen_ratio > image_ratio:
        scaled_width = imageToShow.width * height // imageToShow.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = imageToShow.height * width // imageToShow.width
    image = imageToShow.resize((scaled_width, scaled_height), Image.BICUBIC)
            
    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))

    # Display image.
    device.image(image)



# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D24)
reset_pin = digitalio.DigitalInOut(board.D25)
BAUDRATE = 24000000
spi = board.SPI()

disp = ili9341.ILI9341(spi,rotation=90,cs=cs_pin,dc=dc_pin,rst=reset_pin,baudrate=BAUDRATE) # 2.2", 2.4", 2.8", 3.2" ILI9341

imagenes = ["FinalQR.jpeg","Logo_Identica.jpg","ic_launcher.jpg"]
image_counter = 0

while True :
    image = Image.open("Images/"+imagenes[image_counter])
    show_image (disp,image)
    if (image_counter < (len(imagenes)-1)):
        image_counter += 1
    else:
        image_counter = 0
        
    sleep (2)

"""
# Orgiinal Way 

if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)    # Get drawing object to draw on image.

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image)

"""