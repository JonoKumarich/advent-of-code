from tqdm import tqdm

ValueMap = list[tuple[int, int, int]]


def part_01(input: str) -> str:
    groups = input.split('\n\n')
    
    seeds = [int(seed) for seed in groups[0].split()[1:]]
    maps = build_maps(groups)
    
    location_values = map_seeds(seeds, maps.values())
    return min(location_values)
            


def part_02(input: str) -> str:
    groups = input.split('\n\n')
    
    seed_ranges = [int(seed) for seed in groups[0].split()[1:]]
    maps = build_maps(groups)
    location_values = []
    
    for i, seed_start in enumerate(seed_ranges):
        if i % 2 == 1:
            continue
        
        seed_end = seed_start + seed_ranges[i+1]
        seeds = list(range(seed_start, seed_end))
        
        location_values.extend(map_seeds(seeds, maps.values()))
    
    return min(location_values)


def get_map(groups: list[str], index: int) -> ValueMap:
    return [
        tuple(map(int, line.split())) 
        for line in groups[index].splitlines()[1:]
    ]


def get_map_name(groups: list[str], index: int) -> str:
    full_name = groups[index].splitlines()[0]
    return full_name.split()[0]


def get_mapped_value(input_value: int, map: ValueMap) -> int:
    for destination_start, source_start, length in map:
        source_end = source_start + length
        
        if input_value not in range(source_start, source_end):
            continue
        
        return destination_start + (input_value - source_start)
    
    return input_value
        

def map_seeds(seeds: list[int], maps: list[ValueMap]) -> list[int]:
    location_values = []
    for seed in tqdm(seeds):
        value = seed
        for map in maps:
            value = get_mapped_value(value, map)
        
        location_values.append(value)
        
    return location_values


def build_maps(groups: list[str]):
    map_ranges = range(1, len(groups))
    return {get_map_name(groups, index): get_map(groups, index) for index in map_ranges}
