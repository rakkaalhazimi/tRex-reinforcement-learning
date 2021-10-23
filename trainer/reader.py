from __main__ import config
import re
import tensorflow as tf



class CheckpointReader:

    def __init__(self, **kwargs):
        self.ckpt = tf.train.Checkpoint(**kwargs)
        self.path = "./checkpoints/"
        self.manager = tf.train.CheckpointManager(self.ckpt, self.path, max_to_keep=100)


class LogReader:
    """Catch and parse incoming log message from browser"""

    def __init__(self):
        self.log_pattern = re.compile(r'"(.*)"')
        self.params_pattern = re.compile(r"[0-9\.-]+")

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


class TensorReader:
    """
    Build dynamic-sized tensor that can be write per-time-step. It also support reset utility,
    so that we have a clean tensor in every training episode.

    Heavily rely on tf.TensorArray.

    read about: tf.TensorArray for more information
    """
    
    def __init__(self):
        self.index = 0
        self.action_probs = self.build_tensor()
        self.rewards = self.build_tensor()
        
    def build_tensor(self):
        return tf.TensorArray(dtype=tf.float32, size=0, dynamic_size=True)

    def record(self, action, rewards):
        self.action_probs = self.action_probs.write(self.index, action)
        self.rewards = self.rewards.write(self.index, rewards)
        self.index += 1

    def get_tensor(self):
        return self.action_probs.stack(), self.rewards.stack()

    def reset(self):
        self.__init__()