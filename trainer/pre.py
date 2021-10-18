from __main__ import config

import re
from typing import List

import tensorflow as tf




class Preprocessor:

    def __init__(self):
        self.eps = config.EPS
        self.log_pattern = re.compile(r'"(.*)"')
        self.params_pattern = re.compile(r"[0-9\.]+")


    def list_to_tensor(seq: List):
        """Convert all values inside list to tf.Tensor"""
        seq = [float(num) for num in seq]
        return tf.expand_dims(tf.constant(seq, dtype=tf.float32), axis=0)


    def parse_log(self, message: str):
        """
        Parse browser log message, return list of params if the console doesn't contain
        environment state. Otherwise return None.
        """
        searched = self.log_pattern.search(message)
        if searched:
            numlist = self.params_pattern.findall(searched.group(0))
            return numlist if len(numlist) >= config.PARAM_NUM else None
        return None


    def get_expected_return(
        self,
        rewards: tf.Tensor, 
        gamma: float, 
        standardize: bool = True) -> tf.Tensor:
        """Compute expected returns per timestep."""

        n = tf.shape(rewards)[0]
        returns = tf.TensorArray(dtype=tf.float32, size=n)

        # Start from the end of `rewards` and accumulate reward sums
        # into the `returns` array
        rewards = tf.cast(rewards[::-1], dtype=tf.float32)
        discounted_sum = tf.constant(0.0)
        discounted_sum_shape = discounted_sum.shape
        for i in tf.range(n):
            reward = rewards[i]
            discounted_sum = reward + gamma * discounted_sum
            discounted_sum.set_shape(discounted_sum_shape)
            returns = returns.write(i, discounted_sum)
        returns = returns.stack()[::-1]

        if standardize:
            returns = ((returns - tf.math.reduce_mean(returns)) /
                    (tf.math.reduce_std(returns) + self.eps))

        return returns