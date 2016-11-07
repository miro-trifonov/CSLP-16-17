import parser
import lorry
import bin
import service_area

def create_model(filename):
    parameters = parser.parsefile(filename)
    areas = {}
    for i in range(1, parameters.get('noAreas') + 1):
        truck = lorry.Lorry(parameters.get('lorryVolume'), parameters.get('lorryMaxLoad'), i)
        thrashbin = bin.Bin(parameters.get('binVolume'))
        # TODO area parsing is not correct, yet
        areas[i] = service_area.Area(i, freq, thresh, bins, thrashbin, truck, map)
    return areas
