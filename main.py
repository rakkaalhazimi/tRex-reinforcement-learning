# Std library
import os
import re
import contextlib

# 3rd-party library
import numpy as np
import tensorflow as tf
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Local file
from utils import config
from trainer.pre import Preprocessor


def start_selenium(server: str):
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"browser": "ALL"}
    driver = webdriver.Chrome(desired_capabilities=capabilities)
    driver.get(server)

def start_seed(seed):
    tf.random.set_seed(seed)
    np.random.seed(seed)


class MainApp:

    def __init__(self):
        start_seed(config.SEED)
        start_selenium(config.SERVER)

if __name__ == '__main__':
    app = MainApp()
    
