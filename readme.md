![image of BVG lights in action: radiating strips of LEDs with some on indicating incoming trains](https://michaelweinberg.org/images/bvg_light_annotated.png)

A blogpost explaining how all of this works is available [here](https://michaelweinberg.org/blog/2025/03/08/pi-powered-bvg-alerts/). 


###########to actually run the script

if you are logged in to the pi

1. source env/bin/activate
2. sudo -E env PATH=$PATH python3 bvg_light.py



########neopixel setup
installing the libraries involves a few different steps:

1. Install blinka library to be able to use circutpython: 
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

1a. You need to turn on the virtual environment every time:
'source env/bin/activate'

2. install neopixel library:
https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage

3. do the things required to use sudo for the neopixel library:
https://learn.adafruit.com/python-virtual-environment-usage-on-raspberry-pi/usage-with-sudo

('sudo -E env PATH=$PATH python3 neo_test.py')


4. make it run at startup:

https://learn.adafruit.com/python-virtual-environment-usage-on-raspberry-pi/automatically-running-at-boot
