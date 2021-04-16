import logging

import gym
from gym import error, spaces, utils
from gym.utils import seeding

from lord_gym.envs.space import Map

logger = logging.getLogger(__name__)


class LordEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.space = Map()
        logger.info("Created")

    def step(self, action):
        logger.info(f"Action {action}")

    def reset(self):
        logger.info("Reset")

    def render(self, mode='human'):
        for l in self.space.get_text_representation():
            logger.info(l)

    def close(self):
        logger.info(f"Close")