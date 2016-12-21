import random

i = 1001
biggest_number = 100
percent_no_road = 0.2
output_file = open('matrix.txt', 'w')

for j in range(0, i):
    for k in range(0, i):
        number = 0
        if j == k:
            number = 0
        elif random.random < percent_no_road:
            number = -1
        else:
            number = random.randint(1, biggest_number)
        if not k == i - 1:
            output_file.write('{} '.format(number))
        else:
            output_file.write('{}\n'.format(number))
