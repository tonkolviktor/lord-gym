import logging
from functools import reduce

from gym import spaces

from lord_gym.envs.game import Player
from lord_gym.envs.objects import IdleCitizen, WoodsMan, StoneMan, IronMan

logger = logging.getLogger(__name__)


class Action:
    def __init__(self, subtype_index: int):
        self.subtype_index = subtype_index

    def do_action(self, player: Player):
        raise NotImplementedError()

    @classmethod
    def get_subtypes(cls) -> int:
        raise NotImplementedError()


class NoAction(Action):
    def do_action(self, player: Player):
        pass

    @classmethod
    def get_subtypes(cls) -> int:
        return 1

    def __str__(self):
        return f"No-Action"


class ConvertCitizen(Action):
    pairs = [(IdleCitizen, WoodsMan), (IdleCitizen, StoneMan), (IdleCitizen, IronMan)]
    subtypes = pairs + [(pair[1], pair[0]) for pair in pairs]

    def __init__(self, subtype_index: int):
        (self.from_type, self.to_type) = self.subtypes[subtype_index]

    def do_action(self, player: Player):
        player.replace_object(self.from_type, self.to_type)

    @classmethod
    def get_subtypes(cls) -> int:
        return len(cls.subtypes)

    def __str__(self):
        return f"Action: {self.from_type.__name__} -> {self.to_type.__name__}"


action_order = [NoAction, ConvertCitizen]


def get_action_space():
    return spaces.Discrete(reduce(lambda x, y: x + y, map(lambda x: x.get_subtypes(), action_order)))  # sum up subtypes


def resolve_action(action_orig) -> Action:
    action = action_orig
    for action_class in action_order:
        if action < action_class.get_subtypes():
            return action_class(action)
        action -= action_class.get_subtypes()
    raise ValueError(f"Unknown action: {action_orig}")
