# Std library
import re
import keyboard

# 3rd-party library
import tensorflow as tf

# Local file
from init.selenium_ import driver
from utils import config


# Regex for log message
logmsg = re.compile(r'"(.*)"')
numre = re.compile(r"[0-9\.]+")


# Keyboard Event
keyboard.press_and_release("space")

# Model test
model = tf.keras.layers.Dense(2)

def main_loop():
    step = 0
    while step <= config.EPISODES:
        for entry in driver.get_log("browser"):
            message = logmsg.search(entry["message"])

            if message:
                report_message = message.group(0)
                current_state = numre.findall(report_message)

                if len(current_state) == config.PARAM_NUM:
                    print(current_state)
                    step += 1
    else:
        driver.close()

if __name__ == '__main__':
    main_loop()
    
