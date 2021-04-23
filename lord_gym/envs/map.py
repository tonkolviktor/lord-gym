from typing import List, Optional

from lord_gym.envs.objects import DummyObj, GameObject


class Map:
    SIZE_X = 10
    SIZE_Y = 10

    def __init__(self):
        self._map = [[[] for _ in range(self.SIZE_Y)] for _ in range(self.SIZE_X)]
        [[self.add_object(DummyObj((i, j))) for i in range(self.SIZE_Y)] for j in range(self.SIZE_X)]

    def add_object(self, go: GameObject):
        self._map[go.position_x][go.position_y].append(go)

    def get_text_representation(self) -> List:
        result = ['/' + '-' * len(self._map) + '\\']
        for i in range(len(self._map)):
            result.append('|' + ''.join([self.get_main_object(i, j).representation for j in range(len(self._map[i]))]) + '|')
        result.append('\\' + '-' * len(self._map) + '/')

        return result

    def get_main_object(self, i, j) -> GameObject:
        highest_go: Optional[GameObject] = None
        for go in self._map[i][j]:
            if highest_go is None or highest_go.z_index < go.z_index:
                highest_go = go
        return highest_go

    def step(self, game: 'LordGame'):
        pass
