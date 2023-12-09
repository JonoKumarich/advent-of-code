from itertools import pairwise


def part_01(input: str) -> int:
    readings = [list(map(int, line.split())) for line in input.splitlines()]
    last_readings = [[line[-1]] for line in readings]
    
    for i, line in enumerate(readings):
        values: list[int] = [1]
        while not all(val == 0 for val in values):
            values = [b - a for (a, b) in pairwise(line)]
            last_readings[i].append(values[-1])
            line = values
        
    return sum(sum(history) for history in last_readings)


def part_02(input: str) -> str:
    return "Part two answer"
