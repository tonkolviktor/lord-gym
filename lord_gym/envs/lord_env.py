import logging

import gym
from gym import error, spaces, utils
from gym.utils import seeding

from lord_gym.envs.game import LordGame

logger = logging.getLogger(__name__)


class LordEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.game: LordGame = None
        logger.info("Created")

    def step(self, action):
        logger.info(f"Step {action}")
        if action is not None:
            self.game.do_action(action)
        self.game.step()

    def reset(self):
        self.game = LordGame()
        logger.info("Reset")

    def render(self, mode='human'):
        self.game.render_to_logger()

    def close(self):
        logger.info(f"Close")