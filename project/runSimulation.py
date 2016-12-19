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
    help_file = open("usageInformation.txt", 'r')
    print help_file.read()
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
        event_queue.put((next_service_time, (area, 'startGarbageCollection')))
        for i in area.bins:
            thrashbin = area.bins.get(i)
            next_trash_disposal_time = next_thrash_disposal(0)
            event_queue.put((next_trash_disposal_time, (thrashbin, 'disposeTrash')))

    event_queue.put((parameters.get('warmUpTime'), (0, 'report')))


def make_path(this_area, bin_numbers):
    distance_map = this_area.distance_map
    path = []
    current_position = 0
    while bin_numbers:
        # closest_dist = min(distance_map[current_position].values)
        # bin_number = [key for key, value in dict.iteritems() if value == min_value]
        bin_dist = {}
        for bin_number in bin_numbers:
            current_distance = distance_map[current_position][bin_number]
            bin_dist[current_distance] = bin_number
        smallest_distance = min(bin_dist.keys())
        closest_bin = bin_dist[smallest_distance]
        bin_numbers.remove(closest_bin)
        path.append((closest_bin, smallest_distance))
        current_position = closest_bin
    # path.append((0, distance_map[current_position][0]))
    return path


# garbage collection function
def start_garbage_collection(area, time):
    lorry = area.lorry
    if lorry.travelling:
        lorry.late = True
        return False
    bins = area.bins
    bins_to_be_emptied = []
    for bin_id in bins:
        if bins[bin_id].to_be_emptied:
            bins_to_be_emptied.append(bin_id)
    lorry.path = make_path(area, bins_to_be_emptied)
    lorry.travelling = True
    time_to_next_bin = lorry.path[0][1] / 60.0
    event_queue.put((time + time_to_next_bin, (lorry, 'empty_bin')))
    event_queue.put((time + area.service_frequency, (area, 'startGarbageCollection')))


# Creating and running the simulation
file_name = sys.argv[1]
parameters = my_parser.parse_file(file_name)
if not parameters:
    print "Error"
    sys.exit()
areas = createObjects.create_areas(parameters)
event_queue = Queue.PriorityQueue()
report = False
bag_volume = parameters.get('bagVolume')
service_time = parameters.get('binServiceTime') / 3600.0
empty_lorry_time = 5 * service_time
output_file = open('output.txt', 'w')
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
        print str(time_dhms) + " " + event_type
        if event_type == 'startGarbageCollection':
            area = event_object
            start_garbage_collection(area, time_now)
        elif event_type == 'disposeTrash':
            this_bin = event_object
            bag_weight = random.random() * (
                parameters.get('bagWeightMax') - parameters.get('bagWeightMin')) + parameters.get('bagWeightMin')
            bag = (bag_volume, bag_weight)
            this_bin.add_bag(bag)
            next_disposal_time = next_thrash_disposal(time_now)
            event_queue.put((next_disposal_time, (this_bin, 'disposeTrash')))
            output_file.write(
                "{} -> bag weighting {:.2f} kg disposed of at bin {}\n".format(time_dhms, bag_weight, this_bin.id))
            output_file.write(
                "{} -> load of bin {} became {:.2f} kg and contents volume {:.2f} m^3\n".format(time_dhms, this_bin.id,
                                                                                                this_bin.weight,
                                                                                                this_bin.volume))
            if this_bin.overflow:
                output_file.write("{} -> bin {} overflowed\n".format(time_dhms, this_bin.id))

        elif event_type == 'report':
            report = True
        elif event_type == 'empty_bin':  # TODO consider moving actual bin emptying to other event
            lorry = event_object
            this_bin = areas[lorry.id].bins[lorry.path[0][0]]
            is_last_bin = len(lorry.path) == 1
            emptied = lorry.empty_bin(this_bin)
            output_file.write(
                "{} -> lorry {} arrived at location {}\n".format(time_dhms, lorry.id, this_bin.id))
            if emptied and not is_last_bin:
                time_to_next_bin = lorry.path[0][1] / 60.0
                event_queue.put((time_now + service_time, ((lorry, this_bin.id, emptied), 'leave_location')))
                event_queue.put((time_now + time_to_next_bin + service_time, (lorry, 'empty_bin')))
            else:
                delay = service_time * emptied
                time_to_depo = areas[lorry.id].distance_map[this_bin.short_id][0] / 60.0
                event_queue.put((time_now + delay, ((lorry, this_bin.id, emptied), 'leave_location')))
                event_queue.put((time_now + time_to_depo + delay, (lorry, 'return_to_depo')))
        elif event_type == 'return_to_depo':
            lorry = event_object
            lorry.return_lorry()
            output_file.write(
                "{} -> load of lorry {} became {:.2f} kg and contents volume {:.2f} m^3\n".format(time_dhms, lorry.id,
                                                                                                  0, 0))
            if lorry.path:
                time_to_next_bin = lorry.path[0][1] / 60.0
                event_queue.put((time_now + time_to_next_bin + empty_lorry_time, (lorry, 'empty_bin')))
            elif lorry.late:
                event_queue.put((time_now + empty_lorry_time, (areas[lorry.id], 'startGarbageCollection')))
        elif event_type == "leave_location":
            lorry = event_object[0]
            bin_id = event_object[1]
            lorry_emptied_bin = event_object[2]
            if lorry_emptied_bin:
                output_file.write(
                    "{} -> load of bin {} became {:.2f} kg and contents volume {:.2f} m^3\n".format(time_dhms, bin_id,
                                                                                                    0, 0))
                output_file.write(
                    "{} -> load of lorry {} became {:.2f} kg and contents volume {:.2f} m^3\n".format(time_dhms,
                                                                                                      lorry.id,
                                                                                                      lorry.load,
                                                                                                      lorry.volume))
            output_file.write("{} -> lorry {} left location {}\n".format(time_dhms, event_object[0], event_object[1]))
        else:
            print "error on: " + event_type

output_file.close()
print 'success'
sys.exit(0)
