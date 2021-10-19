import numpy as np

# Init parameter
SERVER = "http://localhost:5500/"
SEED = 42

# Training parameter
NUM_ACTS = 3
UNITS = 128
PARAM_NUM = 6
EPISODES = 2
MIN_CRITERION = 100
GAMMA = 0.99
EPS = np.finfo(np.float32).eps.item()