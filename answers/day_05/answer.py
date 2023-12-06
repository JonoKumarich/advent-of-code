ValueMap = list[tuple[int, int, int]]


def part_01(input: str) -> str:
    groups = input.split('\n\n')
    
    seeds = [int(seed) for seed in groups[0].split()[1:]]
    maps = build_maps(groups)
    
    location_values = map_seeds(seeds, maps.values())
    return min(location_values)


def part_02(input: str) -> str:
    groups = input.split('\n\n')
    
    seed_info = [int(seed) for seed in groups[0].split()[1:]]
    seed_ranges = [(seed_start, seed_info[i+1]) for i, seed_start in enumerate(seed_info) if i % 2 == 0]
    maps = build_maps(groups)
    
    for value_map in maps.values():
        bulk_seed_mappings = []
        
        for seed_start, range_size in seed_ranges:
            # Get bulk ranges for seeds
            bulk_seed_mappings.extend(bulk_seed_map(seed_start, range_size, value_map))
        
        seed_ranges = []
        for mapping in bulk_seed_mappings:
            bin = mapping[2]
            offset = 0 if bin is None else value_map[bin][0] - value_map[bin][1]
            
            # Updated seed_ranges with new bulk mapping translations
            seed_ranges.append((mapping[0] + offset, (mapping[1] + offset) - (mapping[0] + offset)))
        
    return min([seed[0] for seed in seed_ranges])


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
    for seed in seeds:
        value = seed
        for map in maps:
            value = get_mapped_value(value, map)
        
        location_values.append(value)
        
    return location_values


def build_maps(groups: list[str]):
    map_ranges = range(1, len(groups))
    return {get_map_name(groups, index): get_map(groups, index) for index in map_ranges}


def bulk_seed_map(seed_start: int, seed_range: int, value_map: ValueMap) -> list[list[int]]:

    
    current_seed = seed_start
    bulk_seed_maps = []
    
    while current_seed < seed_start + seed_range:
        
        for bin, (_, source_start, length) in enumerate(value_map):
            
            if current_seed in range(source_start, source_start + length):
                bulk_seed_maps.append([current_seed, min(source_start + length, seed_start + seed_range) - 1, bin])
                current_seed = source_start + length
                
                break
            
            if bin == len(value_map) - 1:
                try:
                    next_bin = min(bin[1] for bin in value_map if bin[1] > current_seed)
                except ValueError:
                    # If there is no next bin, go to end of seed range
                    next_bin = seed_start + seed_range
                bulk_seed_maps.append([current_seed, next_bin, None])
                current_seed = next_bin

    return bulk_seed_maps