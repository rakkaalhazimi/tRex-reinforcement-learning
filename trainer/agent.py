from __main__ import config

from typing import Tuple, List
import keyboard

import tensorflow as tf
from tensorflow.keras import layers

from .reader import TensorReader


class Action:
    """Wrapper for keyboard press mapper"""

    def __init__(self):
        self.action_keys = {
            0: self.press_none, 
            1: self.press_up, 
            2: self.press_down
        }

    def __call__(self, key: int):
        move = self.action_keys[key]
        move()

    def press_down(self):
        keyboard.press("down")

    def press_up(self):
        keyboard.release("down")
        keyboard.press_and_release("up")

    def press_none(self):
        keyboard.release("down")



class PolicyGradient(tf.keras.Model):
    """Policy Gradient model that map state into probs of actions."""

    def __init__(self, num_actions: int, num_hidden_units: int):
        """Initialize."""
        super().__init__()

        self.common = layers.Dense(num_hidden_units, activation="relu")
        self.actor = layers.Dense(num_actions, activation="softmax", name="actor")

    def call(self, inputs: tf.Tensor) -> Tuple[tf.Tensor, tf.Tensor]:
        x = self.common(inputs)
        return self.actor(x)


class Agent:
    """An agent that we need to improve from continuous time of training."""

    def __init__(self):
        self.model = PolicyGradient(config.NUM_ACTS, config.UNITS)
        self.action = Action()

    def move(self, probs: tf.Tensor):
        """Commit an action based on probability distribution of actions"""
        # key = int(tf.random.categorical(probs, 1)[0, 0])
        key = int(tf.argmax(probs, axis=1))
        self.action(key)
        return key

    def run(self, state: List[tf.Tensor], rewards: tf.Tensor, recorder: TensorReader) -> List[tf.Tensor]:
        """Record state and do the action"""
        # Feed the state into model
        state = tf.reshape(tf.stack(state, axis=0), (1, -1))
        action = self.model(state)
        
        # Perform action
        key = self.move(action)

        # Record all result tensor
        recorder.record(action=action[0, key], 
                        rewards=rewards)