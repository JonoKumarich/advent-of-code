from itertools import combinations
from functools import lru_cache


NUM_REPEATS = 5


def part_01(input: str) -> int:    
    lines = [line.split() for line in input.splitlines()]
    arrangements = [list(map(int, arrangement.split(','))) for _, arrangement in lines]
    records = [record for record, _ in lines]
    
    total = 0
    for record, arrangement in zip(records, arrangements):
        
        total += calculate_record(tuple(record), tuple(arrangement))
                
    return total


def part_02(input: str) -> int:
    lines = [line.split() for line in input.splitlines()]
    arrangements = [list(map(int, arrangement.split(','))) for _, arrangement in lines]
    records = [record for record, _ in lines]
    
    total = 0
    for record, arrangement in zip(records, arrangements):
        repeated_record: list[str] = []
        repeated_arrangement: list[int] = []
        for i in range(NUM_REPEATS):
            if i != 0:
                repeated_record.append('?')
            repeated_record.extend(record)
            repeated_arrangement.extend(arrangement)    
        
        add = calculate_record(tuple(repeated_record), tuple(repeated_arrangement))
        total += add
        
    return total
    
# Optimisations:

@lru_cache
def calculate_record(remaining_record: tuple[str], remaining_arrangement: tuple[int]) -> int:
    remaining_record = list(remaining_record)
    remaining_arrangement = list(remaining_arrangement)
    
    if len(remaining_arrangement) == 0:
        if any(record == '#' for record in remaining_record):
            return 0
        return 1
    
    if len(remaining_record) == 0:
        return 0
    
    match remaining_record[0]:
        case '.':
            return calculate_record(tuple(remaining_record[1:]), tuple(remaining_arrangement))
        case '?':
            dot_result = calculate_record(tuple(['.'] + remaining_record[1:]), tuple(remaining_arrangement))
            hash_result = calculate_record(tuple(['#'] + remaining_record[1:]), tuple(remaining_arrangement))
            return dot_result + hash_result
            
        case '#':
            # Check for continuous string possible long enough
            if any([val == '.' for val in remaining_record[:remaining_arrangement[0]]]):
                return 0
            
            if remaining_arrangement[0] > len(remaining_record):
                return 0
            
            if remaining_arrangement[0] == len(remaining_record):
                remaining_arrangement.pop(0)
                return calculate_record((), tuple(remaining_arrangement))
            
            if remaining_record[remaining_arrangement[0]] == '#':
                return 0
            
            return calculate_record(tuple(remaining_record[remaining_arrangement[0]+1:]), tuple(remaining_arrangement)[1:])
        case _:
            raise ValueError(f"Invalid value found: '{remaining_record[0]}'")
        
    
    
    

def get_hash_groups(record: str) -> list[int]:
    char_groups: list[int] = []
    running_total = 0
    for char in record:
        if char == '#':
            running_total += 1
            continue
        
        char_groups.append(running_total)
        running_total = 0
    
    char_groups.append(running_total)
    return [char for char in char_groups if char != 0]