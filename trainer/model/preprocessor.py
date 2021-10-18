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




if __name__ == '__main__':
    parser = parse_log()
    result = parser('rakka alhazimi "test: 10, test: 20"')
    print(result)