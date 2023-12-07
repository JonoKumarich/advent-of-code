import math

# TODO: Change from brute force to mathematically calculating bounds
# We should be able to calculate the intersection points between a line and parabola
# Then classify points based on that.

def part_01(input: str) -> str:
    races = parse_races(input)
    num_ways_to_win = []
    
    for total_time, record_distance in races:
        min_hold_time = find_winning_time_bound(total_time, record_distance, 'start')
        max_hold_time = find_winning_time_bound(total_time, record_distance, 'end')
        num_ways_to_win.append(max_hold_time - min_hold_time + 1)
        
    return math.prod(num_ways_to_win)


def part_02(input: str) -> str:
    total_time, record_distance = parse_single_race(input)
    
    min_hold_time = find_winning_time_bound(total_time, record_distance, 'start')
    max_hold_time = find_winning_time_bound(total_time, record_distance, 'end')
        
    return max_hold_time - min_hold_time + 1


def parse_line(line: str) -> list[int]:
    return [int(num) for num in line.split()[1:]]


def parse_races(input: str) -> list[tuple[int, int]]:
    """List of tuples where first element is time, and second element is distance record"""
    lines = [parse_line(line) for line in input.splitlines()]
    transposed_lines = [tuple(race) for race in zip(*lines)]
    return transposed_lines


def parse_single_race(input: str) -> tuple[int, int]:
    # Maybe clean this up for readability
    return [int(''.join(line.split(": ")[1].split())) for line in input.splitlines()]
        

def find_winning_time_bound(total_time: int, record_distance: int, bound: str) -> int:
    if bound not in ['start', 'end']:
        raise ValueError(f"Bound value: {bound} not allowed. Accepted values: 'start', 'end'")
    
    base_range = range(total_time + 1)
    time_range = base_range if bound == 'start' else reversed(base_range)
    
    for hold_time in time_range:
        time_remaining = total_time - hold_time
        if hold_time * time_remaining > record_distance:
            return hold_time

    raise ValueError("No winning time found for these conditions")    
