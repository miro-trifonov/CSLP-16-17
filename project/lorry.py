""" A lorrry. Most of the statistics are collected here and updated at the end of a journey"""

class Lorry:
    def __init__(self, max_volume, max_load, lorry_id):
        self.max_volume = max_volume
        self.max_load = max_load
        self.id = lorry_id
        self.load, self.volume = 0, 0
        self.path = []
        self.travelling = False
        self.late = False
        self.report = False

        self.local_time_traveled = 0
        self.number_of_journeys = [0, 0]  # (total, this schedule)
        self.number_of_schedules = 0
        self.time_traveled = 0
        self.total_volume_collected = 0
        self.total_load_collected = 0



    def schedule_task(self):
        self.travelling = True

    def empty_bin(self, bin_to_empty):
        if self.load + bin_to_empty.weight <= self.max_load and self.volume + bin_to_empty.volume <= self.max_volume:
            self.load += bin_to_empty.weight
            self.volume += bin_to_empty.volume / 2
            bin_to_empty.empty()
            self.path.pop(0)
            return True
        else:
            print "Lorry full"
            return False

    # Total statistic values updated here, in order to collect statistics only for completed journeys
    def return_lorry(self):
        self.total_volume_collected += self.volume
        self.total_load_collected += self.load
        self.time_traveled += self.local_time_traveled
        self.local_time_traveled = 0
        self.volume = 0
        self.load = 0
        self.number_of_journeys[1] += 1
        if not self.path:
            self.travelling = False
            if self.report:
                self.number_of_schedules += 1
                self.number_of_journeys[0] += self.number_of_journeys[1]
                self.number_of_journeys[1] = 0
