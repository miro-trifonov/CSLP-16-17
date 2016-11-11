import sys
# parse_file -> given a filename as an input, parses a bin collection file it into a dictionary,
# provided it has rightly formatted input and prints error otherwise
# validate_input -> called automatically by parse_file this function checks if all needed arguments are given
# and displays warnings for some types of unrealistic input
# num -> makes sure that given argument is int or a float, as specified by num_type

# TODO add check for correct row length in matrix length


def parse_file(filename):
    arguments = {}
    is_valid = True
    expected_global_arguments_int = ['lorryVolume', 'lorryMaxLoad', 'binServiceTime', 'disposalDistrShape', 'noAreas']
    expected_global_arguments_float = ['binVolume', 'disposalDistrRate', 'bagVolume', 'bagWeightMin', 'bagWeightMax',
                                       'stopTime', 'warmUpTime']
    expected_area_arguments = ['serviceFreq', 'thresholdVal', 'noBins']
    area_ids = []
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
        if tokens is [] or tokens[0] == '#':
            continue
        elif road_layout_input == 'expect_arg':
            if tokens[0] == 'roadsLayout':
                road_layout_input = True
                continue
            else:
                print "Error: 'roads layout' required"
                sys.exit(1)
        elif road_layout_input and remaining_road_matrix_len != 0:
            new_list = arguments.get('roadsLayout {}'.format(area_id), [])
            for i in range(1,tokens.__len__()):
                tokens[i] = num(tokens[i], 'roadsLayout', 'int')
                if tokens[i] is False:
                    print "Error \"not an integer\". Possibly caused by missing row in road layout matrix"
                    sys.exit(1)
            new_list.append(tuple(tokens))
            arguments[('roadsLayout {}'.format(area_id))] = new_list
            remaining_road_matrix_len -= 1
            if remaining_road_matrix_len == 0:
                road_layout_input = False
        elif tokens[0] in expected_global_arguments_int and len(tokens) > 1:
            key, value = tokens[0], num(tokens[1], tokens[0], 'int')
            if value is False:
                sys.exit(1)
            arguments[key] = value
            expected_global_arguments_int.remove(key)
            if len(tokens) > 2:
                print "Warning too many arguments given for: " + line
        elif tokens[0] in expected_global_arguments_float and len(tokens) > 1:
            key, value = tokens[0], num(tokens[1], tokens[0], 'float')
            if value is False:
                sys.exit(1)
            arguments[key] = value
            expected_global_arguments_float.remove(key)
            if len(tokens) > 2:
                print "Warning too many arguments given for: " + line
        elif tokens[0] == 'areaIdx':
            area_id = tokens[1]
            area_ids.append(area_id)
            for arg in expected_area_arguments:
                arguments["{} {}".format(arg, area_id)] = num(tokens[tokens.index(arg) + 1], "{} {}".format(arg, area_id), 'float')
            road_layout_input = 'expect_arg'
            remaining_road_matrix_len = int(arguments.get('noBins {}'.format(area_id))) + 1
        else:
            print "Invalid input: " + line
            sys.exit(1)
    parsed_file.close()
    expected_global_arguments = expected_global_arguments_int + expected_global_arguments_float
    is_valid = is_valid and validate_input(arguments, road_layout_input, expected_global_arguments, area_ids)
    if is_valid:
        return arguments
    else:
        return None


def validate_input(arguments, expect_road_input, remaining_global_arguments,areas):
    if expect_road_input:
        print "Error: Road layout matrix missing rows"
        sys.exit(1)
    elif remaining_global_arguments:
        for arg in remaining_global_arguments:
            print "Error: Expected input: {}".format(arg)
        sys.exit(1)
    elif len(areas) is not arguments.get('noAreas'):
        print "Areas given are less then specified"
        sys.exit(1)

    # Warnings: Print warning for some common examples of valid, but unrealistic input
    if arguments.get('lorryVolume') < 2 * arguments.get('binVolume'):
        print "Warning: lorry volume is small"
    if arguments.get('binVolume') < 2 * arguments.get('bagVolume'):
        print "Warning: bin volume is small"
    if arguments.get('lorryMaxLoad') < 2 * arguments.get('bagWeightMax'):
        print "Warning: lorry max load capacity is small"
    for i in areas:
        if arguments.get('serviceFreq {}'.format(i)) < arguments.get('disposalDistrRate') * arguments.get('bagVolume') / arguments.get('binVolume'):
            print "Warning: service frequency may be too small for area number {}".format(i)
    if arguments.get('warmUpTime') > arguments.get('stopTime'):
        print "Warning: warm up time too big"
    if arguments.get('binServiceTime') > 300:
        print "Warning: bin service time may be too big"

    return True


def num(s, key, num_type):
    if num_type is 'int':
        try:
            return int(s)
        except ValueError:
            print "Error: \"{}\" is not an integer in  {}".format(s, key)
            return False
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            print "Error: \"{}\" is not a number in  {}".format(s, key)
            return False
