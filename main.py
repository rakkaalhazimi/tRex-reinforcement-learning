import json
import time
import re
import keyboard
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Regex for log message
logmsg = re.compile(r'".*"')

# Selenium setup
capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"browser": "ALL"}
driver = webdriver.Chrome(desired_capabilities=capabilities)
driver.get("http://127.0.0.1:5500/index.html")

# Keyboard Event
keyboard.press_and_release("space")


# Console.log read
count = 0
while count <= 100:
  for entry in driver.get_log("browser"):
    message = logmsg.search(entry["message"])
    if message:
      jsonmsg = json.loads(message.group(0))
      print(jsonmsg)
      count += 1


# time.sleep(2.0)
driver.close()
