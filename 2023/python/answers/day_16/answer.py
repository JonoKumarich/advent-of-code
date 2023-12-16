def part_01(input: str) -> int:
    grid = [list(line) for line in input.splitlines()]
    
    start = (0, -1)
    direction = (0, 1)
    visited_positions = travel_light_path(grid, start, direction, set())
    
    return len({position for position, _ in visited_positions})


def part_02(input: str) -> int:
    grid = [list(line) for line in input.splitlines()]
    max_visited = 0
    
    for n in range(len(grid)):
        visited_positions = travel_light_path(grid, (n, -1), (0, 1), set())
        max_visited = max(max_visited, len({position for position, _ in visited_positions}))
        
        visited_positions = travel_light_path(grid, (n, len(grid[0])), (0, -1), set())
        max_visited = max(max_visited, len({position for position, _ in visited_positions}))
    
    for m in range(len(grid[0])):
        visited_positions = travel_light_path(grid, (-1, m), (1, 0), set())
        max_visited = max(max_visited, len({position for position, _ in visited_positions}))
        
        visited_positions = travel_light_path(grid, (m, len(grid)), (-1, 0), set())
        max_visited = max(max_visited, len({position for position, _ in visited_positions}))
        
    return max_visited
    

def travel_light_path(
    grid: list[list[str]],
    starting_position: tuple[int, int], 
    starting_direction: tuple[int, int],
    visited_paths: set[tuple[tuple[int, int], tuple[int, int]]]
) -> set[tuple[tuple[int, int], tuple[int, int]]]:

    position, direction = starting_position, starting_direction
    
    while True:
        position = add_positions(position, direction)
        
        # Out of grid bounds
        if min(position) < 0:
            break
        if position[0] >= len(grid):
            break
        if position[1] >= len(grid[0]):
            break
        
        # Visited path before
        if (position, direction) in visited_paths:
            return visited_paths
        
        visited_paths.add((position, direction))
        value = grid[position[0]][position[1]]
        
        match value:
            case '.':
                continue
            case '-':
                if direction[0] == 0:
                    continue
                
                first_split = travel_light_path(grid, position, (0, -1), visited_paths)
                second_split = travel_light_path(grid, position, (0, 1), visited_paths)
                
                visited_paths.update(first_split)
                visited_paths.update(second_split)
                break
            case '|':
                if direction[1] == 0:
                    continue
                
                first_split = travel_light_path(grid, position, (-1, 0), visited_paths)
                second_split = travel_light_path(grid, position, (1, 0), visited_paths)
                
                visited_paths.update(first_split)
                visited_paths.update(second_split)
                break
            case '/':
                direction = change_forwardslash_direction(direction)
            case '\\':
                direction = change_backslash_direction(direction)
            case _:
                raise ValueError(f'Value not found: {value}')
            
    return visited_paths

    
def add_positions(position: tuple[int, int], direction: tuple[int, int]) -> tuple[int, int]:
    return (position[0] + direction[0], position[1] + direction[1])


def change_forwardslash_direction(current_direction: tuple[int, int]) -> tuple[int, int]:
    match current_direction:
        case (1, 0):
            return (0, -1)
        case (-1, 0):
            return (0, 1)
        case (0, 1):
            return (-1, 0)
        case (0, -1):
            return (1, 0)
        case _:
            raise ValueError(f'Invalid Direction: {current_direction}')
        
        
def change_backslash_direction(current_direction: tuple[int, int]) -> tuple[int, int]:
    match current_direction:
        case (1, 0):
            return (0, 1)
        case (-1, 0):
            return (0, -1)
        case (0, 1):
            return (1, 0)
        case (0, -1):
            return (-1, 0)
        case _:
            raise ValueError(f'Invalid Direction: {current_direction}')
