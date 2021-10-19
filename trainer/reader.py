from __main__ import config
import re
import tensorflow as tf



class LogReader:

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
    
    def __init__(self):
        self.index = 0
        self.action_probs = self.build_tensor()
        self.values = self.build_tensor()
        self.rewards = self.build_tensor()
        
    def build_tensor(self):
        return tf.TensorArray(dtype=tf.float32, size=0, dynamic_size=True)

    def record(self, action, values, rewards):
        self.action_probs = self.action_probs.write(self.index, action)
        self.values = self.values.write(self.index, values)
        self.rewards = self.rewards.write(self.index, rewards)
        self.index += 1

    def get_tensor(self):
        return self.action_probs.stack(), self.values.stack(), self.rewards.stack()

    def reset(self):
        self.__init__()