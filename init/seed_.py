"""Set seed number for reproducibility of training"""
import numpy as np
import tensorflow as tf

from ..utils.config import SEED


tf.random.set_seed(SEED)
np.random.seed(SEED)