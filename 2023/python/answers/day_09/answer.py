from itertools import pairwise


def part_01(input: str) -> int:
    readings = parse_input(input)
    last_readings = [[line[-1]] for line in readings]
    
    for i, line in enumerate(readings):
        values: list[int] = [1]
        while not all(val == 0 for val in values):
            values = [b - a for (a, b) in pairwise(line)]
            last_readings[i].append(values[-1])
            line = values
        
    return sum(sum(history) for history in last_readings)


def part_02(input: str) -> int:
    readings = parse_input(input)
    first_readings = [[line[0]] for line in readings]
    for i, line in enumerate(readings):
        values: list[int] = [1]
        while not all(val == 0 for val in values):
            values = [b - a for (a, b) in pairwise(line)]
            first_readings[i].insert(0, values[0])
            line = values
    
    values = []
    for reading in first_readings:
        total = 0
        for value in reading:
            total = value - total
            
        values.append(total)
    
    return sum(values)


def parse_input(input: str) -> list[list[int]]:
    return [
        [int(value) for value in line.split()]
        for line in input.splitlines()
    ]