import bin


# An area class, which contains the information for a service area, as well as all the bins in it

class Area:
    def __init__(self, area_id, service_frequency, threshold, bins, bin_volume, lorry, map):
        self.area_id = area_id
        self.service_frequency = 1.0 / service_frequency
        self.threshold = threshold
        self.lorry = lorry
        self.bins = {}
        for i in range(1, int(bins)):
            a_bin = bin.Bin(bin_volume, self.area_id, i)
            self.bins[i] = a_bin
        self.map = map

    def schedule_service(self):
        self.lorry.schedule_task()
        # maybe do stuff here
