import os

def toggle_keyboard(state):
    if state == "on":
        os.system("./toggle_keyboard.sh -on")
    else:
        os.system("./toggle_keyboard.sh -off")