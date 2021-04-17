import logging

import gym
import unittest

from lord_gym.envs.action import ConvertCitizen
from lord_gym.envs.agent import IronMan, WoodsMan, StoneMan
from lord_gym.envs.lord_env import LordEnv  # does registration

logging.basicConfig(level=logging.INFO)


class LordEnvTest(unittest.TestCase):

    def test_basic(self):
        env = gym.make('lord-v0')
        env.reset()
        a1 = ConvertCitizen(IronMan)
        env.step(a1)
        a2 = ConvertCitizen(WoodsMan)
        env.step(a2)
        a3 = ConvertCitizen(StoneMan)
        env.step(a3)

        for _ in range(20):
            env.step(None)
        env.render()
