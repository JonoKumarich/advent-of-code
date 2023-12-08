import re
import math

MAP_REGEX = r"(\w+)\s*=\s*\((\w+),\s*(\w+)\)"

def part_01(input: str) -> int:
    directions, map_input = input.split('\n\n')
    mappings = parse_map_input(map_input)

    current_code = 'AAA'
    direction_steps = len(directions)
    current_step = 0
    
    while True:
        current_direction = directions[current_step % direction_steps]
        current_step += 1
        
        left, right = mappings[current_code]
        current_code = left if current_direction == 'L' else right
        
        if current_code == 'ZZZ':
            break
        
    return current_step


def part_02(input: str) -> int:
    directions, map_input = input.split('\n\n')
    mappings = parse_map_input(map_input)
    
    starting_positions = [key for key in mappings if key[2] == 'A']
    min_positions: list[int] = []
    
    direction_steps = len(directions)
    
    # We can't calculate this via iteration as 
    # the result number seems to be way too large.
    # 
    # Not 100% sure why, but I have noticed that the Z occurances 
    # for each starting position happen at frequency intervals.
    # We can calculate this frequency for each position and use 
    # the greatest common multiple as the first occurance where all
    # positions equal the success criteria
    for position in starting_positions:
        current_step = 0
        current_code = position
        
        while True:
            current_direction = directions[current_step % direction_steps]
            current_step += 1
            
            left, right = mappings[current_code]
            current_code = left if current_direction == 'L' else right
            
            if current_code[2] == 'Z':
                min_positions.append(current_step)
                break
        
    return math.lcm(*min_positions)


def parse_map_input(map_input: str) -> dict[str, tuple[str, str]]:
    map_codes = [re.findall(MAP_REGEX, m)[0] for m in map_input.splitlines()]
    return {key: (left, right) for (key, left, right) in map_codes}
