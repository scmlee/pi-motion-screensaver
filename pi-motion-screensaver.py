#!/usr/bin/env python3
 
import sys
import time
import RPi.GPIO as io
import subprocess
 
io.setmode(io.BCM)
SHUTOFF_DELAY = 20  # seconds
PIR_PIN = 17        # Pin 11 on the board
LED_PIN = 18
 
def main():
    io.setup(PIR_PIN, io.IN)
    io.setup(LED_PIN, io.OUT)
    turned_off = False
    last_motion_time = time.time()

    #Test the LED
    print("LED test....")
    io.output(LED_PIN, True)
    time.sleep(1)
    io.output(LED_PIN, False)

    print(".")

    while True:
        #print ("Checking... ", time.time(), last_motion_time, io.input(PIR_PIN))
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

        time.sleep(.5)
 
def turn_on():
    io.output(LED_PIN, False)
    print(time.strftime("%D %T"), "-", "Turn monitor on")
    subprocess.call("sh monitor_on.sh", shell=True)
 
def turn_off():
    io.output(LED_PIN, True)
    print(time.strftime("%D %T"), "-", "Turn monitor off")
    subprocess.call("sh monitor_off.sh", shell=True)
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        turn_on();
        io.cleanup()
