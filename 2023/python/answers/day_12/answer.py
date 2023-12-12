from itertools import combinations


def part_01(input: str) -> int:
    '''
    Let's try brute force:
    
    For each row:
        - Calculate number of #'s
        - Calculate number of remaining #'s to allocate
        - For each combination of #'s:
            - Check if that combination then matches the arrangement key
    '''
    
    lines = [line.split() for line in input.splitlines()]
    arrangements = [list(map(int, arrangement.split(','))) for _, arrangement in lines]
    records = [record for record, _ in lines]
    
    total = 0
    for record, arrangement in zip(records, arrangements):
        existing_hashes = record.count('#')
        allocatable_hashes = sum(arrangement) - existing_hashes
        variable_indexes = [i for i, ltr in enumerate(record) if ltr == '?']
        
        for combos in combinations(variable_indexes, allocatable_hashes):
            potential_record = ['#' if n in combos else c for n, c in enumerate(record)]
            potential_record = ''.join(potential_record).replace('?', '.')
            
            if get_hash_groups(potential_record) == arrangement:
                total += 1
                
    return total


def part_02(input: str) -> str:
    return "Part two answer"


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