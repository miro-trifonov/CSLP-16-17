class Bin:
    def __init__(self, max_volume, area_id, bin_id):
        self.max_volume = max_volume
        self.weight, self.volume = 0, 0
        self.id = "{}.{}".format(area_id, bin_id)
        self.overflow = False
        self.full = 0

    def add_bag(self, (bag_volume, bag_weight)):
        if self.overflow:
            return 100
        self.weight += bag_weight
        self.volume += bag_volume
        if self.volume > self.max_volume:
            self.overflow = True
            self.full = 100
        else:
            self.full = self.volume / self.max_volume * 100
        return self.full

    def empty(self):
        self.volume = 0
        self.weight = 0
        self.full = 0
