import numpy as np

# Init parameter
SERVER = "http://localhost:5500/"
SEED = 42

# Training parameter
EPS = np.finfo(np.float32).eps.item()
PARAM_NUM = 6
EPISODES = 10
GAMMA = 0.99