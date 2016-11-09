import math


class Bin:
    def __init__(self, max_volume, ):
        self.max_volume = max_volume
        self.weight, self.volume = 0, 0
        self.full = 0

    def add_bad(self, (bag_volume, bag_weight)):
        self.weight += bag_weight
        self.volume += bag_volume
        if self.volume + bag_volume > self.max_volume:
            self.full = 1
            print 'overflow'
            return 'overflow'
        else:
            self.full = self.volume / self.max_volume  # Make sure this is not an int
            math.floor(self.full * 100)

    def empty(self):
        self.volume = 0
        self.weight = 0
        self.full = 0
