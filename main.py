import board
import busio
import adafruit_ssd1305
import time
from PIL import Image, ImageDraw, ImageFont
import socket
import netifaces
import datetime
import sys, fcntl
import subprocess

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

# Get the currently connected SSID of the Wi-Fi network
def get_wifi_network():
    try:
        output = subprocess.check_output(["iwgetid", "-r"]).decode("utf-8").strip()
        return output
    except subprocess.CalledProcessError:
        return 'Unknown'

# co2sensor

def decrypt(key,  data):
    cstate = [0x48,  0x74,  0x65,  0x6D,  0x70,  0x39,  0x39,  0x65]
    shuffle = [2, 4, 0, 7, 1, 6, 5, 3]
    
    phase1 = [0] * 8
    for i, o in enumerate(shuffle):
        phase1[o] = data[i]
    
    phase2 = [0] * 8
    for i in range(8):
        phase2[i] = phase1[i] ^ key[i]
    
    phase3 = [0] * 8
    for i in range(8):
        phase3[i] = ( (phase2[i] >> 3) | (phase2[ (i-1+8)%8 ] << 5) ) & 0xff
    
    ctmp = [0] * 8
    for i in range(8):
        ctmp[i] = ( (cstate[i] >> 4) | (cstate[i]<<4) ) & 0xff
    
    out = [0] * 8
    for i in range(8):
        out[i] = (0x100 + phase3[i] - ctmp[i]) & 0xff
    
    return out

def hd(d):
    return " ".join("%02X" % e for e in d)

values = {}
def getCo2Content():
    try:
        data = list(fp.read(8))
    except OSError as e:
        print(f"OS error: {e}")
        return 'Unknown', 'Unknown'
    decrypted = None
    if data[4] == 0x0d and (sum(data[:3]) & 0xff) == data[3]:
        decrypted = data
    else:
        decrypted = decrypt(key, data)

    if decrypted[4] != 0x0d or (sum(decrypted[:3]) & 0xff) != decrypted[3]:
            print (hd(data), " => ", hd(decrypted),  "Checksum error")
    else:
            op = decrypted[0]
            val = decrypted[1] << 8 | decrypted[2]
        
            values[op] = val
        
            co2 = values.get(0x50, 'Unknown')
            temp = round(values.get(0x42, 'Unknown')/16.0-273.15,2) if 0x42 in values else 'Unknown'
            return co2, temp

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the SSD1305 OLED class.
disp = adafruit_ssd1305.SSD1305_I2C(128, 32, i2c)

font = ImageFont.truetype('/home/barne/src/co2pi/CourierPrime-Regular.ttf', 12)

# Create blank image for drawing.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

disp.fill(0)
disp.show()

# init co2sensor
key = [0xc4, 0xc6, 0xc0, 0x92, 0x40, 0x23, 0xdc, 0x96]
fp = open("/dev/hidraw0", "a+b",  0)

HIDIOCSFEATURE_9 = 0xC0094806
set_report = [0x00] + key
set_report = bytearray(set_report)
fcntl.ioctl(fp, HIDIOCSFEATURE_9, set_report)

start_time = time.time()

while True:

    if time.time() - start_time < 300:
        # Draw some text.
        # font = ImageFont.load_default()
        # text = "IP: " + get_ip_address()

        text = "SSID: " + get_wifi_network() + " " + str(int(300 - (time.time() - start_time))) + "s"
        co2, temp = getCo2Content()
        text += "\nCO2: " + str(co2) + " ppm" + " @ " + str(temp) + " C"

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        # Write two lines of text.
        draw.text((0, 0), text, font=font, fill=255)

        # Display image.
        disp.image(image)
        disp.show()
    else:
        # turn off display
        disp.fill(0)

    # Wait for one second.
    time.sleep(1)