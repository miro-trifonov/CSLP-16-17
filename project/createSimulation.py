import parser
import lorry
import bin
import service_area


def create_model(parameters):
    areas = {}
    for i in range(0, int(parameters.get('noAreas'))):
        truck = lorry.Lorry(parameters.get('lorryVolume'), parameters.get('lorryMaxLoad'), i)
        thrashbin = bin.Bin(parameters.get('binVolume'))
        freq, thresh, bins, road_map = parameters.get('serviceFreq {}'.format(i)), parameters.get('thresholdVal {}'.format(i)), parameters.get('noBins {}'.format(i)), parameters.get('roadsLayout {}'.format(i)),
        areas[i] = service_area.Area(i, freq, thresh, bins, thrashbin, truck, road_map)
    return areas
