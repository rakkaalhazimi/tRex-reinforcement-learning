# Std library
import os
import re
import contextlib

# 3rd-party library
import keyboard
import numpy as np
import tensorflow as tf
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Local file
from trainer.model import ActorCritic
from trainer.action import Action
from utils import config


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

def list_to_tensor(seq: list):
    """Convert all values inside list to tf.Tensor"""
    seq = [float(num) for num in seq]
    return tf.constant(seq, dtype=tf.float32)



class Agent:

    def __init__(self):
        self.model = ActorCritic(config.NUM_ACTS, config.UNITS)
        self.action = Action()

    def move(self, probs: tf.Tensor):
        key = int(tf.random.categorical(probs, 1)[0, 0])
        print(key)
        self.action(key)


class LogReader:

    def __init__(self):
        self.log_pattern = re.compile(r'"(.*)"')
        self.params_pattern = re.compile(r"[0-9\.]+")

    def read(self, message: str):
        """
        Parse browser log message, return list of params if the console doesn't contain
        environment state. Otherwise return None.
        """
        searched = self.log_pattern.search(message)
        if searched:
            numlist = self.params_pattern.findall(searched.group(0))
            return numlist if len(numlist) >= config.PARAM_NUM else None
        return None




class MainApp:

    def __init__(self):
        start_seed(config.SEED)
        self.driver = start_selenium(config.SERVER)
        self.log_reader = LogReader()
        self.agent = Agent()

        self.loop()

    def loop(self):
        done = False
        keyboard.press_and_release("space")
        
        while not done:
            for entry in self.driver.get_log("browser"):
                params = self.log_reader.read(entry["message"])
                if params:
                    # Record and process parameters
                    *state, reward, crash = list_to_tensor(params)
                    state = tf.reshape(tf.stack(state, axis=0), (1, -1))
                    
                    # Agent take an action
                    action_probs, _ = self.agent.model(state)
                    self.agent.move(action_probs)

                    if crash:
                        done = True

        self.driver.close()

if __name__ == '__main__':
    app = MainApp()
    
