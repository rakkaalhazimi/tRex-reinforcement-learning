import keyboard

def press_down():
    keyboard.press("down")

def press_up():
    keyboard.release("down")
    keyboard.press_and_release("up")

def press_none():
    keyboard.release("down")