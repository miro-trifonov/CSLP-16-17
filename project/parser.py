import numbers


def parsefile(filename):
    if filename is None:
        usage_information = """ To run the program please pass as an argument a file which contains the following:
lorryVolume <uint8 t>
lorryMaxLoad <uint16 t>
binServiceTime <uint16 t>
binVolume <float>
disposalDistrRate <float>
disposalDistrShape <uint8 t>
bagVolume <float>
bagWeightMin <float>
bagWeightMax <float>
noAreas <uint8 t>
areaIdx <uint8 t>
serviceFreq <float>
thresholdVal <float>
noBins <uint16 t>
roadsLayout
0 <int8 t> <int8 t> ... <int8 t>
<int8 t> 0 <int8 t> ... <int8 t>
...
...
...
... ...
<int8 t> <int8 t> <int8 t> ... 0
stopTime <float>
warmUpTime <float>
For comments please begin the line with  #"""
        return usage_information
    arguments = {}
    try:
        parse_file = open(filename)
        matrix_reading_mode = False
        for line in parse_file:
            if line[0] is '#':
                continue
            elif matrix_reading_mode and not (line[0].isdigit() or line[0] == '-'):
                matrix_reading_mode = False
            elif matrix_reading_mode:
                new_values = tuple(map(str.strip, line.split(' ')))
                if arguments.get('roadsLayout') is not None:
                    values = arguments.get('roadsLayout')
                    values.append(new_values)
                else:
                    values = [new_values]
                arguments['roadsLayout'] = values
                continue
            split_line = line.split(" ")
            if split_line.__len__() == 1:
                matrix_reading_mode = True
                continue
            key, value = split_line[0], split_line[1]
            arguments[key.strip()] = value.strip()

        parse_file.close()
        is_valid = validateInput(arguments)
        if is_valid:
            return arguments
        else:
            return None
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)


def validateInput(arguments):
    # TODO experimentation mode
    expexted_args = [('lorryVolume', 'int'), ('lorryMaxLoad', 'int'), ('binServiceTime', 'int'), ('binVolume', 'float'),
                     ('disposalDistrRate', 'float'), ('disposalDistrShape', 'int'),
                     ('bagVolume', 'float'), ('bagWeightMin', 'float'), ('bagWeightMax', 'float'), ('noAreas', 'int'),
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
