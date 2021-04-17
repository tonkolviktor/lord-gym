import logging

from lord_gym.envs.agent import GeneralCitizen
from lord_gym.envs.resources import Inventory, Resource
from lord_gym.envs.space import Map


logger = logging.getLogger(__name__)


class LordGame:
    def __init__(self):
        self.map = Map()
        citizens = [GeneralCitizen((0, 0))] * 5
        self.inventory = Inventory({Resource.GOLD: 100}, {type(citizens[0]): citizens})

    def render_to_logger(self):
        for l in self.map.get_text_representation() + self.inventory.get_text_representation():
            logger.info(l)

    def do_action(self, action):
        action.do_action(self)

    def step(self):
        self.map.step(self)
        self.inventory.step(self)