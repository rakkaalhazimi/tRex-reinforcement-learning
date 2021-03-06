# Std library
import re
import time
import collections


# 3rd-party library
import keyboard
import numpy as np
import tensorflow as tf
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Local file
from utils import config  # config must go first
from utils.logger import log_info, finish_log
from trainer.train import Trainer


def start_seed(seed: int):
    """Seed everything for reproducibility of training"""
    tf.random.set_seed(seed)
    np.random.seed(seed)

def start_selenium(server: str):
    """Start selenium webbrowser that connect to dinogame server"""
    cap = DesiredCapabilities.CHROME
    cap["goog:loggingPrefs"] = {"browser": "ALL"}
    driver = webdriver.Chrome(desired_capabilities=cap)
    driver.get(server)
    return driver


class MainApp:
    """Main application of class, start the application by instantiating this class"""

    def __init__(self):
        # Initiate seed and chrome webdriver
        start_seed(config.SEED)
        self.driver = start_selenium(config.SERVER)
        self.trainer = Trainer(self.driver)

        # Run application loop after the preparation is complete
        self.loop()

    def start_game(self):
        """Trigger dino game with space button"""
        keyboard.press_and_release("space")

    def loop(self):
        """Define what happens on the whole of application runtime"""

        # Initiate episode number for logging purpose
        model_ckpt = 1
        if config.CONTINUE:
            model_ckpt = int(self.trainer.last_ckpt.split("-")[-1])

        # Wait for page to fully loaded
        time.sleep(1)

        # Main system loop
        for episode in range(config.EPISODES):

            self.start_game()
            reward, loss = self.trainer.train_batch()
            
            # Record the rewards per episode
            log_info(
                "Finish episode {} with rewards: {:.2f} and loss: {:>8}".format(episode + model_ckpt, reward, loss)
            )
            if reward > config.MAX_REWARDS:
                break

            # Pause before starting, so that the app has enough time to press space
            time.sleep(2)
        
        # Upon completion, log everything and close the webdriver
        finish_log()
        self.driver.close()




if __name__ == '__main__':
    app = MainApp()
    
    
