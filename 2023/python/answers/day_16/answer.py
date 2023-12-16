import time


def part_01(input: str) -> int:
    grid = [list(line) for line in input.splitlines()]
    
    start = (0, -1)
    direction = (0, 1)
    
    # FIXME: We need to break the endless loops. 
    # When seeing an already visited position & direction combo, we can early return
    visited_positions = travel_light_path(grid, start, direction, set())
    
    positions = {position for position, _ in visited_positions}
    for position in positions:
        grid[position[0]][position[1]] = 'X'
    
    return len({position for position, _ in visited_positions})


def part_02(input: str) -> str:
    return "Part two answer"


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
        
        # print_grid(grid, position)
        
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


def print_grid(grid: list[list[str]], position: tuple[int, int] | None = None) -> None:
    # time.sleep(0.5)
    input()
    
    display_grid = [row[:] for row in grid]
    
    if position is not None:
        display_grid[position[0]][position[1]] = '$'
    
    for row in display_grid[25:65]:
        print(''.join(row))

    print()