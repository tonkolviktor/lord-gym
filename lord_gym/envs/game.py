import logging
from typing import Tuple, List

from lord_gym.envs.objects import IdleCitizen, Castle, GameObject, Resource, Citizen, GoldResource, WoodsMine, StoneMine, IronMine
from lord_gym.envs.map import Map


logger = logging.getLogger(__name__)


class LordGame:
    def __init__(self):
        self.map = Map()
        self.player1 = Player(self, (0, 0))

    def render_to_logger(self):
        for l in self.map.get_text_representation() + list(self.player1.get_text_representation()):
            logger.info(l)

    def do_action(self, action):
        action.do_action(self.player1)

    def step(self):
        # self.map.step(self)
        self.player1.step()


class Player:
    def __init__(self, game: LordGame, start_position: Tuple):
        self.game = game
        self.objects = []

        self.castle = Castle(start_position)
        self.add_object(self.castle)

        self.create_object(IdleCitizen, start_position, 5)
        self.create_object(GoldResource, start_position, 100)
        self.create_object(WoodsMine, start_position, 1)
        self.create_object(StoneMine, start_position, 1)
        self.create_object(IronMine, start_position, 1)

    def create_object(self, object_class, start_position, quantity):
        o = object_class(start_position)
        o.quantity = quantity
        self.add_object(o)

    def step(self):
        _ = [o.step(self) for o in self.objects]

    def add_object(self, go: GameObject):
        self.objects.append(go)  # TODO some struct would be nice which indexes based on class and parent class types
        self.game.map.add_object(go)

    def increase_quantity(self, object_class, new_quantity):
        to_remove = None
        for o in self.objects:
            if type(o) == object_class:
                calculated_quantity = o.quantity + new_quantity
                if calculated_quantity < 0:
                    raise ValueError(f"{object_class} has only {o.quantity} quantity cannot do: {new_quantity}")
                elif calculated_quantity == 0:
                    to_remove = o
                    break
                else:
                    o.quantity += new_quantity
                    return

        if to_remove is not None:
            self.objects.remove(to_remove)
            return

        new_object = object_class(self.castle.position)
        new_object.quantity += new_quantity
        self.add_object(new_object)

    def replace_object(self, from_object_class, to_object_class, from_quantity = 1, to_quentity = 1):
        self.increase_quantity(from_object_class, -from_quantity)
        self.increase_quantity(to_object_class, to_quentity)

    @property
    def resources(self) -> List[Resource]:
        for o in self.objects:
            if isinstance(o, Resource):
                yield o

    @property
    def citizens(self) -> List[Citizen]:
        for o in self.objects:
            if isinstance(o, Citizen):
                yield o

    def get_text_representation(self):
        for object_type in [self.resources, self.citizens]:
            yield ', '.join([str(o) for o in object_type])
