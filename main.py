import board
import busio
import adafruit_ssd1305
import time
from PIL import Image, ImageDraw, ImageFont

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the SSD1305 OLED class.
disp = adafruit_ssd1305.SSD1305_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some text.
font = ImageFont.load_default()
text = time.strftime("%H:%M:%S")
draw.text((0, 0), text, font=font, fill=255)

# Display image.
disp.image(image)
disp.show()