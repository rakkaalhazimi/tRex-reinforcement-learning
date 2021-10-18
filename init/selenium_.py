"""Setup Selenium"""

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"browser": "ALL"}
driver = webdriver.Chrome(desired_capabilities=capabilities)
driver.get("http://127.0.0.1:5500/index.html")