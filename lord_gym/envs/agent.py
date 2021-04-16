class GameObject:
    z_index = 0
    representation = " "

    def __init__(self, position):
        self.position_x = position[0]
        self.position_y = position[1]
        self.position = position

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


class WoodsMan(Citizen):
    pass


class StoneMan(Citizen):
    pass


class IronMan(Citizen):
    pass