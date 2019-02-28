# 9.7-E-Paper-Calendar-software
An adaptation of the E-Paper-Calendar-with-iCal-sync-and-live-weather specifically for the 9.7" E-Paper

Currently in early alpha phase. Made for those who wish to adapt the "E-Paper-Calendar-with-iCal-sync-and-live-weather" software with the 9.7" E-Paper Display from waveshare.

### Disclaimer: Please do not confuse this repo with a fully fledged one. I do not have the 9.7" E-Paper display in my possession so there is absolutely no guarantee that this will even work. Also, I will not take responsibility for anything that is related to this software. Please use at your own risk.

Kind Note: If you wish to assist me in the development of this software, you are free to do so. Any help is welcome.
---------------------------------------------------------------------------------------------------------------------------------------
Info, mainly for myself:
* 9.7inch E-Ink display HAT for Raspberry Pi, 1200×825 resolution, 16 gray scale, USB/SPI/I80/I2C interface


-------------------------------------------------------------------------------------------------------------------------------------
## Main features
* Display the date and a full monthly calendar
* Syncronise events from any online calendar (like google, yahoo etc.)
* Get live weather data (including temperature, humidity, etc.) using openweathermap api

## Hardware required
* 7.5" 3-Colour E-Paper Display (Black, White, Red/Yellow) with driver hat from [waveshare](https://www.waveshare.com/product/7.5inch-e-paper-hat-b.htm)
**or**
* 7.5" 2-Colour E-Paper Display (Black, White) with driver hat from [waveshare](https://www.waveshare.com/product/7.5inch-e-paper-hat.htm)
* Raspberry Pi Zero WH (with headers) (no soldering iron required)
* Or: Raspberry Pi Zero W. In this case, you'll need to solder 2x20 pin GPIO headers yourself
* MicroSD card (min. 4GB)
* MicroUSB cable (for power)
* Something to be used as a case (e.g. a picture frame or a 3D-printed case)

# Setup

## Getting the Raspberry Pi Zero W ready
1. After [flashing Raspbian Stretch (Lite or Desktop)](https://www.raspberrypi.org/downloads/raspbian/), set up Wifi on the Raspberry Pi Zero W by copying the file **wpa_supplicant.conf** (from above) to the /boot directory and adding your Wifi details in that file.
2. Create a simple text document named **ssh** in the boot directory to enable ssh.
3. Expand the filesystem in the Terminal with **`sudo raspi-config --expand-rootfs`**
4. Enable SPI by entering **`sudo sed -i s/#dtparam=spi=on/dtparam=spi=on/ /boot/config.txt`** in the Terminal
5. Set the correct timezone with **`sudo dpkg-reconfigure tzdata`**, selecting the correct continent and then the capital of your country.
6. Reboot to apply changes
7. Optional: If you want to disable the on-board leds of the Raspberry, follow these instructions: 
**[Disable on-board-led](https://www.jeffgeerling.com/blogs/jeff-geerling/controlling-pwr-act-leds-raspberry-pi)**

## Installing required packages for python 3.5 
Execute the following command in the Terminal to install all required packages. This will work on both, Raspbian Stretch with Desktop and Raspbian Stretch lite. 

`bash -c "$(curl -sL https://raw.githubusercontent.com/aceisace/9.7-E-Paper-Calendar-software/master/installer-with-debug?token=AcMG9v5VgKH6YC7k-d9DENt1ANgnfs0Eks5ceBY7wA%3D%3D)"`

If the Installer should fail for any reason, kindly open an issue and paste the error. Thanks.
