import numpy as np

# Init parameter
SERVER = "http://localhost:5500/"
SEED = 42

# Hyperparameter
TRAIN = False                                # Whether or not to train the model, or just do the inference
CONTINUE = False                             # Whether or not to continue from existing checkpoint
EPISODES = 1                              # Number of trials 
MAX_REWARDS = 5e+5                          # Maximum rewards for the agent to accomplish
MAX_KEEP_CKPT = 10                          # Max checkpoint to be kept by ckpt manager

PARAM_NUM = 5                               # Number of state features
NUM_ACTS = 3                                # Number of actions: UP, DO NOTHING, DOWN
UNITS = 128                                 # Number of hidden layers
LEARNING_RATE = 1e-2                        # Learning rate for optimizers
GAMMA = 0.99                                # Discount factor for rewards
EPS = np.finfo(np.float32).eps.item()       # Small positive number