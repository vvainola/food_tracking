#! /bin/bash
#This script toggle the virtual keyboard
PID=`pidof matchbox-keyboard`
#Turn keyboard off if first arguments is -off and keyboard is currently turned on
if [[ $1 = -off && "" -ne $PID ]]; then
    killall matchbox-keyboard
#Turn keyboard on if first argument is -on and keyboard is not currently turned on
elif [[ $1 = -on &&  $PID = "" ]]; then
    matchbox-keyboard&
    sleep .1
    wmctrl -r "Keyboard" -b add,above
    MATCHBOX_ID=$(xdotool search --onlyvisible --name Keyboard)
    xdotool windowsize $MATCHBOX_ID 600 250
    xdotool windowmove $MATCHBOX_ID 200 290 
fi