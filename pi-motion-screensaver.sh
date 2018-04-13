#!/bin/bash

#Disable DPMS and prevent screen from blanking
if [ -n "$DISPLAY" ]; then
   echo "DISPLAY is set. Setting DPMS flags..."
   xset s off -dpms
fi

trap "echo Killing child processes; pkill -P $$;" EXIT

python3 pi-motion-screensaver.py 900 > pi-motion-screensaver.log

