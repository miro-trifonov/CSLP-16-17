import numbers


def parsefile(filename):
    if filename is None:
        usage_information = "something"
        return usage_information
    arguments = {}
    expected_global_arguments = ['lorryVolume', 'lorryMaxLoad', 'binServiceTime', 'binVolume', 'disposalDistrRate',
                                 'disposalDistrShape', 'bagVolume', 'bagWeightMin', 'bagWeightMax', 'noAreas',
                                 'stopTime', 'warmUpTime']
    expected_area_arguments = ['serviceFreq', 'thresholdVal', 'noBins']
    try:
        parse_file = open(filename)

    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        return False
    road_layout_input = False
    remaining_road_matrix_len = 0
    area_id = -1
    for line in parse_file:
        tokens = map(str.strip, line.split())
        if tokens[0] is '#':
            continue
        elif tokens[0] in expected_global_arguments and len(tokens) > 1:
            key, value = tokens[0], tokens[1]
            arguments[key] = value
            expected_global_arguments.pop(key)
            if len(tokens) > 2:
                print "Warning too many arguments given for: " + line
        elif tokens[0] == 'areaIdx':
            area_id = tokens[1]
            for arg in expected_area_arguments:
                # TODO is that error catching good enough
                arguments[(expected_global_arguments, area_id)] = tokens[tokens.index(arg) + 1]
            road_layout_input = 'soon'
            remaining_road_matrix_len = arguments.get('noBins') + 1
        elif road_layout_input is 'soon':
            road_layout_input = True
            continue
        elif road_layout_input and remaining_road_matrix_len != 0:
            arguments[('roadsLayout', area_id)] = arguments.get(('roadsLayout', area_id), []).append(tuple(tokens))
            remaining_road_matrix_len -= 1
            if remaining_road_matrix_len is 0:
                road_layout_input = False
        else:
            print "Invalid input: " + line
        parse_file.close()
        is_valid = validateInput(arguments, road_layout_input)
        if is_valid:
            return arguments
        else:
            return None


def validateInput(arguments, road_mode_not_finished):
    # TODO experimentation mode
    global_arguments = [('lorryVolume', 'int'), ('lorryMaxLoad', 'int'), ('binServiceTime', 'int'),
                        ('binVolume', 'float'),
                        ('disposalDistrRate', 'float'), ('disposalDistrShape', 'int'),
                        ('bagVolume', 'float'), ('bagWeightMin', 'float'), ('bagWeightMax', 'float'),
                        ('noAreas', 'int'),
                        ('areaIdx', 'int'), ('serviceFreq', 'float'), ('thresholdVal', 'float'),
                        ('noBins', 'int'), ('roadsLayout', 'matrix'), ('areaIdx', 'int'), ('stopTime', 'float'),
                        ('warmUpTime', 'float'), ]
    parse_problems = arguments.__len__() != expexted_args.__len__()
    if parse_problems is True:
        return "Invalid number of arguments"

    for key in expexted_args:
        argument = arguments.get(key[0])
        if argument is None:
            parse_problems = True
            # will that work for python 2.7
            print '{} not specified'.format(key[0])
        else:
            if key[1] is 'int' and not argument.is_integer():
                print '{} should be integer'.format(key[0])
            elif key[1] is 'float' and not isinstance(argument, numbers.Number):
                print '{} should be float'.format(key[0])
            elif key[1] is 'matrix' and verifyIntegers(argument):
                print '{} should be a matrix'  # TODO
                # Note: the current configuration does not require the parameters to be in correct order, so I'm not checking for that

    if parse_problems is True:
        return True
    else:
        return False


def verifyIntegers(argument):
    for row in argument:
        for number in row:
            number.isdigit()
