
class Area:

    def __init__(self, area_id, service_frequency, threshold, bins, thrashbin, lorry, map):
        self.area_id = area_id
        self.service_frequency = service_frequency
        self.threshold = threshold
        self.lorry = lorry
        self.bins = {}
        for i in range(1, int(bins)):
            self.bins[i] = thrashbin
        self.map = map

    def schedule_service(self):
        self.lorry.schedule_task()
        # maybe do stuff here