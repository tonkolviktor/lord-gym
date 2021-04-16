import logging

import gym
import unittest

from lord_gym.envs.lord_env import LordEnv  # does registration

logging.basicConfig(level=logging.INFO)


class LordEnvTest(unittest.TestCase):

    def test_basic(self):
        env = gym.make('lord-v0')
        env.reset()
        env.render()