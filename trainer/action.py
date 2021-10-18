import keyboard

class Action:
    
    def __init__(self):
        self.action_keys = {
            0: self.press_none, 
            1: self.press_up, 
            2: self.press_down
        }

    def press_down(self):
        keyboard.press("down")

    def press_up(self):
        keyboard.release("down")
        keyboard.press_and_release("up")

    def press_none(self):
        keyboard.release("down")

    def __call__(self, key: int):
        move = self.action_keys[key]
        move()
