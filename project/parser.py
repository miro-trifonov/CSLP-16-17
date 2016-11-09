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
# def validateInput(arguments, road_mode_not_finished):
#     # TODO experimentation mode
#     return True
#     # global_arguments = [('lorryVolume', 'int'), ('lorryMaxLoad', 'int'), ('binServiceTime', 'int'),
#     #                     ('binVolume', 'float'),
#     #                     ('disposalDistrRate', 'float'), ('disposalDistrShape', 'int'),
#     #                     ('bagVolume', 'float'), ('bagWeightMin', 'float'), ('bagWeightMax', 'float'),
#     #                     ('noAreas', 'int'),
#     #                     ('areaIdx', 'int'), ('serviceFreq', 'float'), ('thresholdVal', 'float'),
#     #                     ('noBins', 'int'), ('roadsLayout', 'matrix'), ('areaIdx', 'int'), ('stopTime', 'float'),
#     #                     ('warmUpTime', 'float'), ]
#     # parse_problems = arguments.__len__() != expexted_args.__len__()
#     # if parse_problems is True:
#     #     return "Invalid number of arguments"
#     #
#     # for key in expexted_args:
#     #     argument = arguments.get(key[0])
#     #     if argument is None:
#     #         parse_problems = True
#     #         # will that work for python 2.7
#     #         print '{} not specified'.format(key[0])
#     #     else:
#     #         if key[1] is 'int' and not argument.is_integer():
#     #             print '{} should be integer'.format(key[0])
#     #         elif key[1] is 'float' and not isinstance(argument, numbers.Number):
#     #             print '{} should be float'.format(key[0])
#     #         elif key[1] is 'matrix' and verifyIntegers(argument):
#     #             print '{} should be a matrix'  # TODO
#     #             # Note: the current configuration does not require the parameters to be in correct order, so I'm not checking for that
#     #
#     # if parse_problems is True:
#     #     return True
#     # else:
#     #     return False
#
#
# def verify_integers(argument):
#     for row in argument:
#         for number in row:
#             number.isdigit()

