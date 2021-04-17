from typing import List

from lord_gym.envs.agent import GameObject, Castle, WoodsObj, StoneObj, IronObj, DummyObj


class Map:
    SIZE_X = 10
    SIZE_Y = 10

    def __init__(self):
        self._map = [[[] for _ in range(self.SIZE_Y)] for _ in range(self.SIZE_X)]
        [[self.create_object(DummyObj((i, j))) for i in range(self.SIZE_Y)] for j in range(self.SIZE_X)]
        self.castle = Castle((0, 0))
        self.create_object(self.castle)
        self.create_object(WoodsObj((0, 9)))
        self.create_object(StoneObj((9, 9)))
        self.create_object(IronObj((9, 0)))

    def create_object(self, go: GameObject):
        self._map[go.position_x][go.position_y].append(go)

    def get_text_representation(self) -> List:
        result = ['/' + '-' * len(self._map) + '\\']
        for i in range(len(self._map)):
            result.append('|' + ''.join([self.get_main_object(i, j).representation for j in range(len(self._map[i]))]) + '|')
        result.append('\\' + '-' * len(self._map) + '/')

        return result

    def get_main_object(self, i, j) -> GameObject:
        highest_go = None
        for go in self._map[i][j]:
            if highest_go is None or highest_go.z_index < go.z_index:
                highest_go = go
        return go

    def step(self, game: 'LordGame'):
        pass
