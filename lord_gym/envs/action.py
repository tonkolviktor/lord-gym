import logging

from lord_gym.envs.agent import GeneralCitizen
from lord_gym.envs.game import LordGame

logger = logging.getLogger(__name__)


class Action:
    def do_action(self, game: LordGame):
        raise NotImplementedError()


class ConvertCitizen(Action):
    def __init__(self, to_type, from_type = GeneralCitizen):
        self.to_type = to_type
        self.from_type = from_type

    def do_action(self, game: LordGame):
        if len(game.inventory.citizens.get(self.from_type, [])) <= 0:
            logger.debug(f"No citizen convertion be available {self.from_type.__name__}")
        game.inventory.citizens[self.from_type].pop()
        citizens = game.inventory.citizens.get(self.to_type, [])
        citizens.append(self.to_type(game.map.castle.position))
        game.inventory.citizens[self.to_type] = citizens