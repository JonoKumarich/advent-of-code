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
    
    seed_info = [int(seed) for seed in groups[0].split()[1:]]
    seed_ranges = [(seed_start, seed_info[i+1]) for i, seed_start in enumerate(seed_info) if i % 2 == 0]
    maps = build_maps(groups)
    
    # We need to try and process in bulk here
    # Let's try and think in terms of seed ranges
    # If a portion of a seed range fits into a single mapping range, 
    # then we can simply shift the whole range by the difference from source -> destination
    bulk_seed_mappings = []
    for seed_start, range_size in seed_ranges:
        # Get bulk ranges for seeds
        bulk_seed_mappings.extend(bulk_seed_map(seed_start, range_size, maps))
        
    return bulk_seed_mappings
        
        

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


def bulk_seed_map(seed_start: int, seed_range: int, maps: list[ValueMap]) -> list[list[int]]:
    current_seed = seed_start
    bulk_seed_maps = []
    
    while current_seed < seed_start + seed_range:
        
        for bin, (_, source_start, length) in enumerate(maps['seed-to-soil']):
            
            if current_seed in range(source_start, source_start + length):
                bulk_seed_maps.append([current_seed, min(source_start + length, seed_start + seed_range) - 1, bin])
                current_seed = source_start + length
                
                break
            
            if bin == len(maps['seed-to-soil']) - 1:
                # only if in last element of loop
                next_bin = min(bin[1] for bin in maps['seed-to-soil'] if bin[1] > current_seed)
                bulk_seed_maps.append([current_seed, next_bin, None])
                current_seed = next_bin

    return bulk_seed_maps