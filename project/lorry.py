import bin


class Lorry:
    def __init__(self, max_volume, max_load, lorry_id):
        self.max_volume = max_volume
        self.max_load = max_load
        self.id = lorry_id
        self.load, self.volume = 0, 0
        self.travelling = False

    def schedule_task(self):
        self.travelling = True

    def empty_bin(self, bin_to_empty):
        if self.load + bin_to_empty.load < self.max_load and self.volume + bin_to_empty.volume < self.max_volume:
            self.load += bin_to_empty.load
            self.volume += bin_to_empty.volume / 2
            bin_to_empty.empty()
            return True
        else:
            print "Lorry full"
            return False

    def return_lorry(self):
        self.volume = 0
        self.load = 0
        self.travelling = False
