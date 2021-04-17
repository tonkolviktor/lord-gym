from enum import Enum, auto


class Resource(Enum):
    GOLD = auto()
    IRON = auto()
    STONE = auto()
    WOOD = auto()


class Inventory:
    def __init__(self, start_resources, start_citizens):
        self.resources = start_resources
        self.citizens = start_citizens

    def get_text_representation(self):
        return [', '.join([f'{k}: {self.resources[k]}' for k in self.resources.keys()]),
         ', '.join([f'{k.__name__}: {len(self.citizens[k])}' for k in self.citizens.keys()])]

    def step(self, game: 'LordGame'):
        for c_type in self.citizens:
            for c in self.citizens[c_type]:
                c.step(game)
