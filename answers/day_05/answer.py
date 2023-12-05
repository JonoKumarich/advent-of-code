from collections import defaultdict


def part_01(input: str) -> str:
    groups = input.split('\n\n')
    seeds = [int(seed) for seed in groups[0].split()[1:]]
    
    map_ranges = range(1, len(groups))
    maps = {get_map_name(groups, index): get_map(groups, index) for index in map_ranges}
    
    location_values = []
    for seed in seeds:
        value = seed
        for map in maps.values():
            value = get_mapped_value(value, map)
        
        location_values.append(value)
        
    return min(location_values)
            


def part_02(input: str) -> str:
    return "Part two answer"


def get_map(groups: list[str] ,index: int) -> list[list[int]]:
    return [
        tuple(map(int, line.split())) 
        for line in groups[index].splitlines()[1:]
    ]


def get_map_name(groups: list[str] ,index: int) -> str:
    full_name = groups[index].splitlines()[0]
    return full_name.split()[0]


def get_mapped_value(input_value: int, map: list[tuple[int, int, int]]) -> int:
    for destination_start, source_start, length in map:
        source_end = source_start + length
        
        if input_value not in range(source_start, source_end):
            continue
        
        return destination_start + (input_value - source_start)
    
    return input_value
        