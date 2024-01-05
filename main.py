import board
import busio
import adafruit_ssd1305
import time
from PIL import Image, ImageDraw, ImageFont
import socket
import netifaces
import datetime

current_time = datetime.datetime.now()
print("Starting ", current_time)

# Function to get the IP address
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except:
        return ""

# Get the currently connected Wi-Fi network
def get_wifi_network():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface.startswith('wlan'):
            addresses = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addresses:
                for address in addresses[netifaces.AF_INET]:
                    if 'addr' in address:
                        return address['addr']
    return None

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the SSD1305 OLED class.
disp = adafruit_ssd1305.SSD1305_I2C(128, 32, i2c)

# Create blank image for drawing.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

while True:
    # Clear display.
    disp.fill(0)
    disp.show()

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Draw some text.
    font = ImageFont.load_default()
    text = "IP: " + get_ip_address()
    text = "SSID: " + get_wifi_network()
    draw.text((0, 0), text, font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.show()

    # Wait for one second.
    time.sleep(1)