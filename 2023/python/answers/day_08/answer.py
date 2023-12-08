import re

MAP_REGEX = r"(\w+)\s*=\s*\((\w+),\s*(\w+)\)"

def part_01(input: str) -> int:
    directions, map_input = input.split('\n\n')
    map_codes = [re.findall(MAP_REGEX, m)[0] for m in map_input.splitlines()]
    mappings = {key: (left, right) for (key, left, right) in map_codes}

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


def part_02(input: str) -> str:
    return "Part two answer"
