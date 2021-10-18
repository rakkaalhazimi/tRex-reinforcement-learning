from __main__ import config
from .model import ActorCritic
from .pre import Preprocessor

import re
from typing import Tuple, List

import tensorflow as tf
from tensorflow.keras import layers





class ModelInterface:

    def __init__(self):
        self.pre = Preprocessor()
        self.model = ActorCritic()
        self.loss = self.get_loss_function()

    def get_optimizer(self):
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)

    def get_loss_function(self):
        return tf.keras.losses.Huber(reduction=tf.keras.losses.Reduction.SUM)

    def compute_loss(
        self, 
        action_probs: tf.Tensor, 
        values: tf.Tensor, 
        returns: tf.Tensor) -> tf.Tensor:
        """Computes the combined actor-critic loss."""

        advantage = returns - values

        action_log_probs = tf.math.log(action_probs)
        actor_loss = -tf.math.reduce_sum(action_log_probs * advantage)
        critic_loss = self.loss(values, returns)

        return actor_loss + critic_loss


    