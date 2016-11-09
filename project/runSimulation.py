import createSimulation
# import parser
import Queue
import random
import math


def parse_file(filename):
    arguments = {}
    expected_global_arguments = ['lorryVolume', 'lorryMaxLoad', 'binServiceTime', 'binVolume', 'disposalDistrRate',
                                 'disposalDistrShape', 'bagVolume', 'bagWeightMin', 'bagWeightMax', 'noAreas',
                                 'stopTime', 'warmUpTime']
    expected_area_arguments = ['serviceFreq', 'thresholdVal', 'noBins']
    try:
        parsed_file = open(filename)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        return False
    road_layout_input = False
    remaining_road_matrix_len = 0
    area_id = -1
    for line in parsed_file:
        tokens = map(str.strip, line.split())
        if tokens[0] is '#':
            continue
        elif tokens[0] in expected_global_arguments and len(tokens) > 1:
            key, value = tokens[0], tokens[1]
            arguments[key] = value
            expected_global_arguments.remove(key)
            if len(tokens) > 2:
                print "Warning too many arguments given for: " + line
        elif tokens[0] == 'areaIdx':
            area_id = tokens[1]
            for arg in expected_area_arguments:
                arguments["{} {}".format(arg, area_id)] = tokens[tokens.index(arg) + 1]
            road_layout_input = 'expect_arg'
            remaining_road_matrix_len = int(arguments.get('noBins {}'.format(area_id))) + 1
        elif road_layout_input is 'expect_arg':
            road_layout_input = True
            continue
        elif road_layout_input and remaining_road_matrix_len != 0:
            new_list = arguments.get('roadsLayout {}'.format(area_id), [])
            new_list.append(tuple(tokens))
            arguments[('roadsLayout {}'.format(area_id))] = new_list
            remaining_road_matrix_len -= 1
            if remaining_road_matrix_len is 0:
                road_layout_input = False
        else:
            print "Invalid input: " + line
    parsed_file.close()
    #is_valid = validateInput(arguments, road_layout_input)
    is_valid = True
    if is_valid:
        return arguments
    else:
        return None#



# TODO call that with input
parameters = parse_file("input.txt")
areas = createSimulation.create_model(parameters)
time = 0
event_queue = Queue.PriorityQueue()
report = False
bin_volume = parameters.get('binVolume')
output = []


def next_thrash_disposal(current_time):
    new_time = float(current_time)
    for k in range(0, int(parameters.get('disposalDistrShape'))):
        q = float(parameters.get('disposalDistrRate'))
        log = float(math.log(random.random()))
        new_time += q * log * (-1)
    return new_time


def schedule_first_events():
    for i in range(0, areas.__len__()):
        area = areas[i]
        next_service_time = area.service_frequency
        event_queue.put((next_service_time, (area, 'collectGarbage')))
        for thrashbin in area.bins:
            next_trash_disposal_time = next_thrash_disposal(0)
            event_queue.put((next_trash_disposal_time, (thrashbin, 'disposeTrash')))
    event_queue.put((parameters.get('warmUpTime'), 'report'))


def start_garbage_collection(truck):
    return True

schedule_first_events()

while time < parameters.get('stopTime'):
    event = event_queue.get()
    time_now = event[0]
    if time_now > parameters.get('stopTime'):
        break
    else:
        object = event[1][1]
        event_type = event[1][0]
        if event_queue == 'collectGarbage':
            start_garbage_collection(object)
        elif event_queue == 'disposeTrash':
            this_bin = object
            bag = (bin_volume, random.randint(parameters.get('bagWeightMin'),parameters.get('bagWeightMax')))
            this_bin.add_bag(bag)
            next_disposal_time = next_thrash_disposal(time_now)
            event_queue.put(next_disposal_time, (this_bin, 'disposeTrash'))




