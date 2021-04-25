import logging

import gym
from gym import error, spaces, utils
from gym.utils import seeding

from lord_gym.envs import actions
from lord_gym.envs.error import InvalidGameOperation
from lord_gym.envs.game import LordGame

logger = logging.getLogger(__name__)


class LordEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    action_space = actions.get_action_space()
    max_rounds = 20

    def __init__(self):
        self.game: LordGame = None
        self.rounds_left: int = None
        logger.info("Created")

    def step(self, action):
        logger.info(f"Step {action}")
        assert self.rounds_left > 0
        assert action is not None
        self.rounds_left -= 1

        try:
            self.game.do_action(actions.resolve_action(action))
            self.game.step()
        except InvalidGameOperation as e:
            logger.warning(e)
        observations, info = self.game.observations()
        reward = 1
        done = self.rounds_left == 0
        return observations, reward, done, info

    def reset(self):
        self.game = LordGame()
        self.rounds_left = self.max_rounds
        logger.info("Reset")

    def render(self, mode='human'):
        self.game.render_to_logger()

    def close(self):
        logger.info(f"Close")