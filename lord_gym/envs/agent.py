from lord_gym.envs.resources import Resource


class GameObject:
    z_index = 0
    representation = " "

    def __init__(self, position):
        self.position_x = position[0]
        self.position_y = position[1]
        self.position = position

    def step(self, game: 'LordGame'):
        pass


class DummyObj(GameObject):
    representation = ' '


class Castle(GameObject):
    z_index = 100
    representation = 'C'


class WoodsObj(GameObject):
    representation = 'W'


class StoneObj(GameObject):
    representation = 'S'


class IronObj(GameObject):
    representation = 'I'


class Citizen(GameObject):
    representation = 'x'
    z_index = 50


class GeneralCitizen(Citizen):
    pass


class WorkMan(Citizen):
    work_duration = 5
    resource = None
    quantity = 1

    def __init__(self, position):
        super().__init__(position)
        self.work_done = 0

    def step(self, game: 'LordGame'):
        assert self.resource is not None

        self.work_done += 1
        if self.work_done < self.work_duration:
            return

        self.work_done = 0
        stored = game.inventory.resources.get(self.resource, 0)
        game.inventory.resources[self.resource] = stored + self.quantity


class WoodsMan(WorkMan):
    resource = Resource.WOOD
    quantity = 10


class StoneMan(WorkMan):
    resource = Resource.STONE
    quantity = 10


class IronMan(WorkMan):
    work_duration = 7
    resource = Resource.IRON
    quantity = 5
