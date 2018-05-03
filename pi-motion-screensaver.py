#!/usr/bin/env python3 
 
import sys
import time
import RPi.GPIO as io
import subprocess
import logging 
from logging.handlers import RotatingFileHandler
 
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler('pi-motion-screensaver-logger.log', maxBytes=(2000 * 1024), backupCount=10)
logger.addHandler(handler)

io.setmode(io.BCM)
SHUTOFF_DELAY = 15 * 60  # seconds
PIR_PIN = 17        # Pin 11 on the board


print(time.strftime("%D %T"), "-", "Starting up...")

if len(sys.argv) > 1:
    print("Using argument value as shut-off delay", sys.argv[1], "seconds")
    SHUTOFF_DELAY = int(sys.argv[1])

print("SHUTOFF_DELAY=", str(SHUTOFF_DELAY))
 
def main():
    io.setup(PIR_PIN, io.IN)
    turned_off = False
    last_motion_time = time.time()

    while True:
        logger.debug("Time.time(): ", str(time.time()), ", PIR:", str(io.input(PIR_PIN)), ", last_motion_time: ", str(last_motion_time))
        if io.input(PIR_PIN):
            last_motion_time = time.time()
            sys.stdout.flush()
            if turned_off:
                turned_off = False
                turn_on()
        else:
            if not turned_off and time.time() > (last_motion_time + SHUTOFF_DELAY):
                turned_off = True
                turn_off()

        time.sleep(1)
 
def turn_on():
    logger.info(time.strftime("%D %T"), "-", "Turn monitor on")
    print(time.strftime("%D %T"), "-", "Turn monitor on")
    subprocess.call("sh monitor_on.sh", shell=True)
 
def turn_off():
    logger.info(time.strftime("%D %T"), "-", "Turn monitor off")
    print(time.strftime("%D %T"), "-", "Turn monitor off")
    subprocess.call("sh monitor_off.sh", shell=True)
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        turn_on();
        io.cleanup()
