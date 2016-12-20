import lorry
import service_area


""" Using the simulation params, creates the necessary service areas, bins and lorries """


def create_areas(parameters):
    areas = {}
    for i in range(0, parameters.get('noAreas')):
        truck = lorry.Lorry(parameters.get('lorryVolume'), parameters.get('lorryMaxLoad'), i)
        bin_volume = parameters.get('binVolume')
        freq, thresh, bins, road_map = parameters.get('serviceFreq {}'.format(i)), parameters.get(
            'thresholdVal {}'.format(i)), parameters.get('noBins {}'.format(i)), parameters.get(
            'roadsLayout {}'.format(i))
        areas[i] = service_area.Area(i, freq, thresh, bins, bin_volume, truck, road_map)
    return areas
