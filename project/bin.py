import math


class Bin:
    def __init__(self, max_volume, area_id, bin_id):
        self.max_volume = max_volume
        self.weight, self.volume = 0, 0
        self.id = "{}.{}".format(area_id, bin_id)
        self.overflow = False

    def add_bag(self, (bag_volume, bag_weight)):
        self.weight += bag_weight
        self.volume += bag_volume
        if self.volume > self.max_volume:
            self.overflow = True
        else:
            self.full = self.volume / self.max_volume  # Make sure this is not an int
            math.floor(self.full * 100)

    def empty(self):
        self.volume = 0
        self.weight = 0
        self.full = 0
