import Queue
import math
import random
import sys

import createObjects
import my_parser

# This program runs a simulation of a garbage disposal and collection in a city.
# It expects as an input, the name of a text file which contains the simulation parameters.
# The result from the simulation is then printed in a file called "output.txt" in the program's folder
#
# If ran with no arguments, usage information will be printed

if len(sys.argv) == 1:
    file = open("usageInformation.txt", 'r')
    print file.read()
    sys.exit(0)


# Event time and event schedule functions
def next_thrash_disposal(current_time):
    new_time = float(current_time)
    for k in range(0, parameters.get('disposalDistrShape')):
        rate = 1 / float(parameters.get('disposalDistrRate'))
        log = math.log(random.random())
        new_time += rate * log * (-1)
    return new_time


def schedule_first_events():
    for i in range(0, areas.__len__()):
        area = areas[i]
        next_service_time = area.service_frequency
        event_queue.put((next_service_time, (area, 'collectGarbage')))
        for i in area.bins:
            thrashbin = area.bins.get(i)
            next_trash_disposal_time = next_thrash_disposal(0)
            event_queue.put((next_trash_disposal_time, (thrashbin, 'disposeTrash')))

    event_queue.put((parameters.get('warmUpTime'), (0, 'report')))


# garbage collection function TODO
def start_garbage_collection(truck):
    return True


# Creating and running the simulation
file_name = sys.argv[1]
parameters = my_parser.parse_file(file_name)
areas = createObjects.create_areas(parameters)
event_queue = Queue.PriorityQueue()
report = False
bag_volume = parameters.get('bagVolume')
output = []

schedule_first_events()

while 1 and not event_queue.empty():
    event = event_queue.get()
    time_now = event[0]
    seconds = time_now * 3600
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    d, h, m, s = map(int, [d, h, m, s])
    time_dhms = "{:02d}:{:02d}:{:02d}:{:02d}".format(d, h, m, s)
    if time_now > parameters.get('stopTime'):
        break
    else:
        event_type = event[1][1]
        event_object = event[1][0]
        if event_type == 'collectGarbage':
            start_garbage_collection(event_object)
        elif event_type == 'disposeTrash':
            this_bin = event_object
            bag_weight = random.random() * (
                parameters.get('bagWeightMax') - parameters.get('bagWeightMin')) + parameters.get('bagWeightMin')
            bag = (bag_volume, bag_weight)
            overflown = this_bin.add_bag(bag)
            next_disposal_time = next_thrash_disposal(time_now)
            event_queue.put((next_disposal_time, (this_bin, 'disposeTrash')))
            output.append(
                "{} -> bag weighting {:.2f} kg disposed of at bin {}".format(time_dhms, bag_weight, this_bin.id))
            output.append(
                "{} -> load of bin {} became {:.2f} kg and contents volume {:.2f} m^3".format(time_dhms, this_bin.id,
                                                                                              this_bin.weight,
                                                                                              this_bin.volume))
            if this_bin.overflow:
                output.append("{} -> bin {} overflowed".format(time_dhms, this_bin.id))

        elif event_type == 'report':
            report = True
        else:
            print "error"
output_file = open('output.txt', 'w')
for line in output:
    print>> output_file, line
output_file.close()
print 'success'
sys.exit(0)
