import logging

import gym
import unittest

from lord_gym.envs.lord_env import LordEnv  # does registration

logging.basicConfig(level=logging.DEBUG)


class LordEnvTest(unittest.TestCase):

    def test_basic(self):
        env = gym.make('lord-v0')
        env.reset()

        for a in [1, 2, 3]:
            print(a, env.step(a))

        # for _ in range(20):
        #     env.step(None)
        env.render()
