import logging

from lord_gym.envs.game import Player
from lord_gym.envs.objects import IdleCitizen

logger = logging.getLogger(__name__)


class Action:
    def do_action(self, player: Player):
        raise NotImplementedError()


class ConvertCitizen(Action):
    def __init__(self, to_type, from_type=IdleCitizen):
        self.to_type = to_type
        self.from_type = from_type

    def do_action(self, player: Player):
        player.replace_object(self.from_type, self.to_type)
