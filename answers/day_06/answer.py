import math


def part_01(input: str) -> str:
    races = parse_races(input)
    num_ways_to_win = []
    
    for race in races:
        start, end = calculate_winning_range(race)
        num_ways_to_win.append(end - start + 1)
        
    return math.prod(num_ways_to_win)


def parse_line(line: str) -> list[int]:
    return [int(num) for num in line.split()[1:]]


def parse_races(input: str) -> list[tuple[int, int]]:
    """List of tuples where first element is time, and second element is distance record"""
    lines = [parse_line(line) for line in input.splitlines()]
    return [tuple(race) for race in zip(*lines)]


def calculate_winning_range(race: tuple[int, int]) -> tuple[int, int]:
    min_hold_time = 0
    max_hold_time = 0
    
    total_time, record_distance = race
    
    # Find min_hold
    for hold_time in range(total_time + 1):
        time_remaining = total_time - hold_time
        if hold_time * time_remaining > record_distance: # Assuming we have to better the time and not match it
            min_hold_time = hold_time
            break
        
    # Find max_hold
    for hold_time in reversed(range(total_time + 1)):
        time_remaining = total_time - hold_time
        if hold_time * time_remaining > record_distance:
            max_hold_time = hold_time
            break
    
    return min_hold_time, max_hold_time
        
    

def part_02(input: str) -> str:
    return "Part two answer"
