import numpy as np

# Init parameter
SERVER = "http://localhost:5500/"
SEED = 42

# Hyperparameter
TRAIN = True
CONTINUE = True
EPISODES = 187
MAX_REWARDS = 5e+5

PARAM_NUM = 6
NUM_ACTS = 3
UNITS = 128
LEARNING_RATE = 1e-2
GAMMA = 0.99
EPS = np.finfo(np.float32).eps.item()