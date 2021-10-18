import re
from typing import List

import tensorflow as tf

from ...utils import config


def parse_log():
    """
    Parse console.log from browser with initialized regex patterns. Instead of declaring re.compile
    multiple times, it's a good practice to initialized them in the closure, thus it'll not collide
    with global variables.

    Usage:
        parser = parse_log()
        result = parser("Your console.log message here")

    Return:
        None      -> if the message doesn't contain game state parameter
        List[str] -> otherwise
    """
    # Compile regex
    logmsg = re.compile(r'"(.*)"')
    params = re.compile(r"[0-9\.]+")

    def parse(message: str) -> List[str]:
        searched = logmsg.search(message)
        if searched:
            numlist = params.findall(searched.group(0))
            return numlist if len(numlist) >= config.PARAM_NUM else None
        return None

    return parse


def list_to_tensor(seq: List):
    """Convert all values inside list to tf.Tensor"""
    seq = [float(num) for num in seq]
    return tf.expand_dims(tf.constant(seq, dtype=tf.float32), axis=0)


def get_expected_return(
    rewards: tf.Tensor, gamma: float, standardize: bool = True) -> tf.Tensor:
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
                   (tf.math.reduce_std(returns) + eps))

    return returns


if __name__ == '__main__':
    parser = parse_log()
    result = parser('rakka alhazimi "test: 10, test: 20"')
    print(result)