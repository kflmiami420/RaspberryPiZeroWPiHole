#RaspberryPiZeroWPiHole

# Copyright (c) 2017 Adafruit Industries
# Author: Ladyada, Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FIT NESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

# Modified 8/6/2019 by Mike Corrigan
#  To alternate display of PiHole and System data

# Import Python System Libraries
import json
import subprocess
import time

# Import Requests Library
import requests

# Import Blinka
from board import SCL, SDA
import busio
import adafruit_ssd1306

# Import Python Imaging Library
from PIL import Image, ImageDraw, ImageFont

# URL to get PiHole data
api_url = 'http://localhost/admin/api.php'

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# y coordinate of each of the four rows
y_coord = [-3, 8, 16, 24]
#top = -3

# Load nice silkscreen font
font = ImageFont.truetype('/home/pi/slkscr.ttf', 8)

CPU_LOOPCNT = 14        # gathering CPU data takes longer than the PIHOLE data
PIHOLE_LOOPCNT = 16

loopcnt = PIHOLE_LOOPCNT 
display_cpu = False

# clear the image buffer
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Fixed text for System Stats
CPU_TEXT = "CPU: "
MEM_TEXT = "MEM: "
DSK_TEXT = "DISK: "

# Fixed text for PIHOLE Stats
DNS_TEXT = "DNS Queries: "
ADS_TEXT = "Ads Blocked: "
CLI_TEXT = "Clients: "

# Compute the length of the longest of the fixed text lines
# for the System stats.  This allows the numbers to line up
# in a nice column
tlen = draw.textsize( CPU_TEXT, font=font)
syslen = tlen[0]
tlen = draw.textsize( MEM_TEXT, font=font)
if tlen[0] > syslen :
  syslen = tlen[0]
tlen = draw.textsize( DSK_TEXT, font=font)
if tlen[0] > syslen :
  syslen = tlen[0]

# Compute the length of the longest of the fixed text lines
# for the PiHole stats. 
tlen = draw.textsize( DNS_TEXT, font=font)
pihlen = tlen[0]
tlen = draw.textsize( ADS_TEXT, font=font)
if tlen[0] > pihlen :
  pihlen = tlen[0]
tlen = draw.textsize( CLI_TEXT, font=font)
if tlen[0] > pihlen :
  pihlen = tlen[0]

# Shell scripts for system monitoring from here :
# https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load

cmd = "hostname -I | cut -d\' \' -f1 | tr -d \'\\n\'"
IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
cmd = "hostname | tr -d \'\\n\'"
HOST = subprocess.check_output(cmd, shell=True).decode("utf-8")

# Loop forever displaying the stats
while True:
  while loopcnt > 0 :
    loopcnt = loopcnt - 1

    # Draw a black filled box to clear the image
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # draw the unchanging IP address and hostname
    draw.text((0, y_coord[0]), "IP: " + str(IP) + " " + HOST, font=font, fill=255)

    if display_cpu :

      # Gather system data
      cmd = "cat /proc/loadavg | awk " \
            "'{printf \"%.0f%%\", $3*100}'"
      CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")

      cmd = "free -m | awk 'NR==2{printf " \
            "\"%.0f%% of %s MB\", $3*100/$2, $2 }'"
      MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")

      cmd = "df -h | awk '$NF==\"/\"{printf " \
            "\"%s of %d GB\", $5, $2}'"
      Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

      draw.text((0, y_coord[1]),  CPU_TEXT, font=font, fill=255)
      draw.text((0, y_coord[2]), MEM_TEXT, font=font, fill=255)
      draw.text((0, y_coord[3]), DSK_TEXT, font=font, fill=255)

      draw.text((syslen, y_coord[1]),   str(CPU),      font=font, fill=255)
      draw.text((syslen, y_coord[2]),  str(MemUsage), font=font, fill=255)
      draw.text((syslen, y_coord[3]),  str(Disk),     font=font, fill=255)

    else :
      # Gather PiHole data
      try:
        r = requests.get(api_url)
        data = json.loads(r.text)
        DNSQUERIES = data['dns_queries_today']
        ADSBLOCKED = data['ads_blocked_today']
        CLIENTS = data['unique_clients']
      except KeyError:
        time.sleep(1)
        continue


      draw.text((0, y_coord[1]), DNS_TEXT, font=font, fill=255)
      draw.text((0, y_coord[2]), ADS_TEXT, font=font, fill=255)
      draw.text((0, y_coord[3]), CLI_TEXT, font=font, fill=255)
     
      draw.text((pihlen, y_coord[1]), str(DNSQUERIES), font=font, fill=255)
      draw.text((pihlen, y_coord[2]), str(ADSBLOCKED), font=font, fill=255)
      draw.text((pihlen, y_coord[3]), str(CLIENTS),    font=font, fill=255)


    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(.2)

  # 3 seconds is up

  if display_cpu :
    display_cpu = False
    loopcnt = PIHOLE_LOOPCNT
  else :
    display_cpu = True
    loopcnt = CPU_LOOPCNT
