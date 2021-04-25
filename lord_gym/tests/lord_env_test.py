import logging

import gym
import unittest

from lord_gym.envs.lord_env import LordEnv  # does registration

logging.basicConfig(level=logging.INFO)


class LordEnvTest(unittest.TestCase):

    def test_basic(self):
        env = gym.make('lord-v0')
        env.reset()
        a1 = env.action_space.sample()
        env.step(a1)
        a2 = env.action_space.sample()
        env.step(a2)
        a3 = env.action_space.sample()
        env.step(a3)
        #
        # for _ in range(20):
        #     env.step(None)
        env.render()
