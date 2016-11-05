import math


class Bin:
    def __init__(self, max_volume, ):
        self.max_volume = max_volume
        self.weight, self.volume = 0, 0
        self.full = 0

    def add_bad(self, bag_volume, bag_weight):
        self.weight += bag_weight
        self.volume += bag_volume
        self.full = self.volume / self.max_volume  # Make sure this is not an int
        if self.volume > self.max_volume:
            self.full = 1
            return 'overflow'
        else:
            return math.floor(self.full * 100)

    def empty(self):
        self.volume = 0
        self.weight = 0
        self.full = 0
