# Adafruit 128x32 Oled Bonnet

import time
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

# Create the I2C interface.
disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some text.
font = ImageFont.load_default()
text = time.strftime("%H:%M:%S")
draw.text((0, 0), text, font=font, fill=255)

# Display image.
disp.image(image)
disp.display()