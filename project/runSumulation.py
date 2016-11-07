import createSimulation
import parser
import  Queue
import random

#TODO call that with input
areas = createSimulation.create_model('filename')
parameters = parser.parsefile('filename')
time = 0
event_queue = Queue.PriorityQueue
report = False
bin_volume = parameters.get('binVolume')
report = []

def schedule_first_events:
    for area in areas:
        time = area.service_frequency
        event_queue.put(time, (area, 'collectGarbage'))
        for thrashbin in area.bins
            time = #TODO
            event_queue.put(time, (thrashbin, 'disposeTrash'))
    event_queue.put(parameters.get('warmUpTime'), 'report')


schedule_first_events()

while time < parameters.get('stopTime'):
    event = event_queue.get()
    if event[0] > parameters.get('stopTime'):
        break
    else:
        object = event[1][1]
        event_type = event[1][0]
        if event_queue == 'collectGarbage':
            start_garbage_collection(object)
        elif event_queue == 'disposeTrash':
            bag = (bin_volume, random.randint(parameters.get('bagWeightMin'),parameters.get('bagWeightMax')))
            object.add_bag(bag)
            # TODO schedule next bag disposal event




