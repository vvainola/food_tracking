#! /bin/bash
source \./src/gui/convert.sh
rsync -avzh ./src/ pi@192\.168\.1\.183\:/home/pi/work/food\_tracker/
ssh pi@192.168.1.183 "export FRAMEBUFFER=/dev/fb0; export DISPLAY=:0; echo $DISPLAY; python3.4 /home/pi/work/food_tracker/main.py -pi"
# Kill all food tracker processes and toggle keyboard off
ssh pi@192.168.1.183 "ps -ef | grep python3.4\ /home/pi/work/food_tracker/main.py | grep -v grep | awk '{print \$2}' | xargs kill -9; ./toggle_keyboard.sh -off"