#!/bin/bash
#This script toggle the virtual keyboard
PID=`pidof matchbox-keyboard`
if [ ! -e $PID ]; then
    killall matchbox-keyboard
else
    matchbox-keyboard&
    sleep .1
    MATCHBOX_ID=$(xdotool search --onlyvisible --name Keyboard)
    xdotool windowsize $MATCHBOX_ID 600 250
    xdotool windowmove $MATCHBOX_ID 200 100 
fi