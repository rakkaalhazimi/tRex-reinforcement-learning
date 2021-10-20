from __main__ import config
from typing import List

import tensorflow as tf

from .reader import LogReader, TensorReader, CheckpointReader
from .agent import Agent


optimizer = tf.keras.optimizers.Adam(learning_rate=0.01, clipvalue=1.0)
huber_loss = tf.keras.losses.Huber(reduction=tf.keras.losses.Reduction.SUM)


def list_to_tensor(seq: List[str]):
    """Convert all values inside list to tf.Tensor"""
    seq = [float(num) for num in seq]
    return tf.constant(seq, dtype=tf.float32)


def get_expected_return(
        rewards: tf.Tensor, 
        gamma: float, 
        standardize: bool = True) -> tf.Tensor:
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
                (tf.math.reduce_std(returns) + config.EPS))

    return returns


def compute_loss(
        action_probs: tf.Tensor, 
        values: tf.Tensor, 
        returns: tf.Tensor) -> tf.Tensor:
    """Computes the combined actor-critic loss."""

    advantage = returns - values

    action_log_probs = tf.math.log(action_probs)
    actor_loss = -tf.math.reduce_sum(action_log_probs * advantage)
    critic_loss = huber_loss(values, returns)
    # print(actor_loss, critic_loss)

    return actor_loss + critic_loss


class Trainer:
    """Reinforcement learning trainer, govern everything about the agent's training"""

    def __init__(self, driver):
        """Initiate agent, reader and checkpoint"""
        self.driver = driver
        self.agent = Agent()
        self.log_reader = LogReader()
        self.recorder = TensorReader()
        self.checkpoint = CheckpointReader(model=self.agent.model, optimizer=optimizer)

        # Check last checkpoint
        self.last_ckpt = self.checkpoint.manager.latest_checkpoint
        if self.last_ckpt:
            self.checkpoint.ckpt.restore(self.last_ckpt)    



    def run_episode(self):
        done = False
        while not done:
            for entry in self.driver.get_log("browser"):
                params = self.log_reader.read(entry["message"])
                if params:
                    # Record and process parameters
                    *state, reward, crash = list_to_tensor(params)
                        
                    # Agent will record the state and take an action
                    self.agent.run(state, reward, self.recorder)

                    if crash:
                        action_probs, values, rewards = self.recorder.get_tensor()
                        self.recorder.reset()
                        done = True
                        
        return action_probs, values, rewards


    def train_batch(self):

        with tf.GradientTape() as tape:
            # Run one episode and get the values
            action_probs, values, rewards = self.run_episode()

            # Calculate expected returns
            returns = get_expected_return(rewards, config.GAMMA)

            # Convert training data to appropriate TF tensor shapes
            action_probs, values, returns = [
                tf.expand_dims(x, 1) for x in [action_probs, values, returns]]

            # Calculating loss values to update our network
            loss = compute_loss(action_probs, values, returns)
            print(loss)

        # Compute the gradients from the loss
        grads = tape.gradient(loss, self.agent.model.trainable_variables)

        # Apply the gradients to the model's parameters
        optimizer.apply_gradients(zip(grads, self.agent.model.trainable_variables))

        # Save model and optimizer checkpoints
        self.checkpoint.manager.save()

        episode_reward = tf.math.reduce_sum(rewards)

        return episode_reward