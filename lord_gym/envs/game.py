import logging
from typing import Tuple, List, Dict

from lord_gym.envs.error import InvalidGameOperation
from lord_gym.envs.objects import IdleCitizen, Castle, GameObject, Resource, Citizen, GoldResource, WoodsMine, StoneMine, IronMine, Mine, WorkMan
from lord_gym.envs.map import Map


logger = logging.getLogger(__name__)


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


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

    def observations(self):
        return self.player1.observations()

    def calculate_reward(self):
        return self.player1.calculate_reward()

    def is_game_over(self):
        return self.player1.is_winner()


class Player:
    def __init__(self, game: LordGame, start_position: Tuple):
        self.max_experience = 25
        self.prev_experience = 0
        self.game = game
        self.objects = []

        self.castle = Castle(start_position)
        self.add_object(self.castle)

        self.create_object(IdleCitizen, start_position, 5)
        self.create_object(GoldResource, start_position, 0)
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

    def increase_quantity(self, object_class, new_quantity, dry_run=False):
        if issubclass(object_class, WorkMan):
            workman = self.citizens_dict.get(object_class)
            workman_quantity = 0 if workman is None else workman.quantity
            mine = self.mines_dict.get(object_class.resource_mine_class)
            if mine is None or mine.quantity <= workman_quantity:
                raise InvalidGameOperation("Not enough mines for the workman")

        to_remove = None
        for o in self.objects:
            if type(o) != object_class:
                continue
            calculated_quantity = o.quantity + new_quantity
            if calculated_quantity < 0:
                raise InvalidGameOperation(f"{object_class} has only {o.quantity} quantity cannot do: {new_quantity}")
            elif calculated_quantity == 0:
                to_remove = o
                break

            if not dry_run:
                o.quantity += new_quantity
            return

        if new_quantity < 0:
            raise InvalidGameOperation("Cannot start with reducing new object")

        if dry_run:
            return

        if to_remove is not None:
            self.objects.remove(to_remove)
            return

        new_object = object_class(self.castle.position)
        new_object.quantity += new_quantity
        self.add_object(new_object)

    def replace_object(self, from_object_class, to_object_class, from_quantity = 1, to_quantity = 1):
        self.increase_quantity(from_object_class, -from_quantity, dry_run=True)
        self.increase_quantity(to_object_class, to_quantity, dry_run=True)

        self.increase_quantity(from_object_class, -from_quantity, dry_run=False)
        self.increase_quantity(to_object_class, to_quantity, dry_run=False)

    def calculate_reward(self) -> int:
        new_exp = self.experience
        reward = new_exp - self.prev_experience

        # if self.prev_experience < self.max_experience <= new_exp:  # boost for winning
        #     reward += self.max_experience

        self.prev_experience = new_exp
        return reward

    @property
    def experience(self) -> int:
        experience = 0
        for mine in self.mines:
            workman = self.citizens_dict.get(mine.workman_class)
            if workman is None:
                continue
            experience += workman.quantity * workman.produce_quantity_per_citizen
        return experience

    def is_winner(self):
        return self.experience >= self.max_experience

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

    @property
    def mines(self) -> List[Mine]:
        for o in self.objects:
            if isinstance(o, Mine):
                yield o

    @property
    def resources_dict(self) -> Dict:
        return self.to_dict(self.resources)

    @property
    def citizens_dict(self) -> Dict:
        return self.to_dict(self.citizens)

    @property
    def mines_dict(self) -> Dict:
        return self.to_dict(self.mines)

    def get_text_representation(self):
        for object_type in [self.resources, self.citizens]:
            yield ', '.join([str(o) for o in object_type])

    @staticmethod
    def to_dict(items):
        return {type(k): k for k in items}

    @staticmethod
    def to_quantity_dict(items):
        return {type(k): k.quantity for k in items}

    def observations(self):
        observations = []
        info = {}

        for (objects, object_class) in [(self.resources, Resource), (self.citizens, Citizen), (self.mines, Mine)]:
            resources_dict = self.to_quantity_dict(objects)
            for cls in all_subclasses(object_class):
                q = resources_dict.get(cls, 0)
                observations.append(q)
                info[cls.__name__] = q

        return observations, info
