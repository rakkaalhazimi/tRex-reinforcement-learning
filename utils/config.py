import numpy as np

# Init parameter
SERVER = "http://localhost:5500/"
SEED = 42
TRAIN = True
CONTINUE = False
MAX_REWARDS = 5e+4

# Training parameter
NUM_ACTS = 3
UNITS = 128
PARAM_NUM = 6
EPISODES = 500
LEARNING_RATE = 1e-2
GAMMA = 0.99
EPS = np.finfo(np.float32).eps.item()