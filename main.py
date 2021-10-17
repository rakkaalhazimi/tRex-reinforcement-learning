# Std library
import re
import keyboard

# 3rd-party library
import tensorflow as tf
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Local file
from py_backend.preprocessor import list_to_tensor

PARAM_NUM = 6
EPISODES = 10

# Regex for log message
logmsg = re.compile(r'"(.*)"')
numre = re.compile(r"[0-9\.]+")

# Selenium setup
capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"browser": "ALL"}
driver = webdriver.Chrome(desired_capabilities=capabilities)
driver.get("http://127.0.0.1:5500/index.html")

# Keyboard Event
keyboard.press_and_release("space")

# Model test
model = tf.keras.layers.Dense(2)

def main_loop():
    step = 0
    while step <= EPISODES:
        for entry in driver.get_log("browser"):
            message = logmsg.search(entry["message"])

            if message:
                report_message = message.group(0)
                current_state = numre.findall(report_message)

                if len(current_state) == PARAM_NUM:
                    print(model(list_to_tensor(current_state)))
                    step += 1
    else:
        driver.close()

if __name__ == '__main__':
    main_loop()
    
