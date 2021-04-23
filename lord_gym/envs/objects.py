class GameObject:
    z_index = 0
    quantity = 0
    representation = " "

    def __init__(self, position):
        self.position_x = position[0]
        self.position_y = position[1]
        self.position = position

    def step(self, player: 'Player'):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}: {self.quantity}"


class DummyObj(GameObject):
    representation = ' '


class Castle(GameObject):
    z_index = 100
    quantity = 1
    representation = 'C'

# ------------ Mines ------------------------------


class Mine(GameObject):
    workman_class = None
    representation = 'M'


class WoodsMine(Mine):
    representation = 'W'

    def __init__(self, position):  # workman defined later
        super().__init__(position)
        self.workman_class = WoodsMan


class GoldMine(Mine):
    representation = 'G'

    def __init__(self, position):  # workman defined later
        super().__init__(position)
        self.workman_class = GoldMan


class StoneMine(Mine):
    representation = 'S'

    def __init__(self, position):  # workman defined later
        super().__init__(position)
        self.workman_class = StoneMan


class IronMine(Mine):
    representation = 'I'

    def __init__(self, position):  # workman defined later
        super().__init__(position)
        self.workman_class = IronMan

# ------------- Resources -----------------------------


class Resource(GameObject):
    representation = 'r'


class WoodsResource(Resource):
    representation = 'w'


class GoldResource(Resource):
    representation = 'g'


class StoneResource(Resource):
    representation = 's'


class IronResource(Resource):
    representation = 'i'


# ------------- Citizens -----------------------------


class Citizen(GameObject):
    representation = 'x'
    z_index = 50


class IdleCitizen(Citizen):
    pass


class WorkMan(Citizen):
    work_duration = 5
    resource_class = None
    produce_quantity_per_citizen = 1

    def __init__(self, position):
        super().__init__(position)
        self.work_done = 0

    def step(self, player: 'Player'):
        assert self.resource_class is not None

        self.work_done += 1
        if self.work_done < self.work_duration:
            return

        self.work_done = 0
        player.increase_quantity(self.resource_class, self.produce_quantity_per_citizen * self.quantity)


class WoodsMan(WorkMan):
    resource_class = WoodsResource
    produce_quantity_per_citizen = 10


class StoneMan(WorkMan):
    resource_class = StoneResource
    produce_quantity_per_citizen = 10


class IronMan(WorkMan):
    work_duration = 7
    resource_class = IronResource
    produce_quantity_per_citizen = 5


class GoldMan(WorkMan):
    work_duration = 500
    resource_class = GoldResource
    produce_quantity_per_citizen = 5
