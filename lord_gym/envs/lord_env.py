import logging

import gym
from gym import error, spaces, utils
from gym.utils import seeding

logger = logging.getLogger(__name__)


class LordEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        logger.info("Created")

    def step(self, action):
        logger.info(f"Action {action}")

    def reset(self):
        logger.info("Reset")

    def render(self, mode='human'):
        logger.info(f"Render {mode}")

    def close(self):
        logger.info(f"Close")