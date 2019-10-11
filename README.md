# RaspberryPiZeroWPiHole
RaspberryPiZeroWPiHole
One to show the PiHole stats and one to show system stats

* Download the latest 'Lite' Raspbian to your computer
* Burn the Lite Raspbian to your micro SD card using your computer
* Re-plug the SD card into your computer (don't use your Pi yet!) and set up your wifi connection by editing supplicant.conf
* Activate SSH support
* Plug the SD card into the Pi Zero W
* If you have an HDMI monitor we recommend connecting it up via the mini HDMI adapter we provide in the budget pack - so you can see that   it's booting OK
* Plug in power to the Pi Zero W - you will see the green LED flicker a little. The Pi Zero will reboot while it sets up so wait a good 10   minutes
* If you are running Windows on your computer, install Bonjour support so you can use .local names, you'll need to reboot Windows after     installation
* You can then ssh into raspberrypi.local

* Time to install Pi hole

* in a terminal type the following.                type this ---->    curl -sSL https://install.pi-hole.net | bash


 To install the library for the Pi OLED, enter the following into the terminal:


* sudo pip3 install adafruit-circuitpython-ssd1306

* sudo apt-get install python3-pip

* sudo apt-get install python3-pil

* sudo pip3 install requests


* next you need a font installed 

*cd ~
*wget http://kottke.org/plus/type/silkscreen/download/silkscreen.zip
*unzip silkscreen.zip
