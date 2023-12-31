RELATIVE_POSITIONS = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
START_CHAR = 'S'

def part_01(input: str) -> int:
    grid = [list(line) for line in input.splitlines()]
    start = find_start(grid)
    
    first_step = find_first_step(grid, start)
    previous_direction = (-first_step[0], -first_step[1])
    current_position = add_tuples(start, first_step)
    counter = 1
    
    while True:
        next_direction = find_next_direction(grid, current_position, previous_direction)
        if next_direction is None: 
            break
        
        previous_direction = (-next_direction[0], -next_direction[1])
        current_position = add_tuples(current_position, next_direction)
        counter += 1
        
    return round(counter / 2)



def part_02(input: str) -> int:
    """
    Logic Flow:
        For each row, scan each spot.
        All non-pipe spots are "O" until first pipe section
        Then all non-pip spots are "I" until next pipe section
        etc etc
    """
    grid = [list(line) for line in input.splitlines()]
    pipe_positions: list[list[str | None]] = [[None for _ in row] for row in grid]
    start = find_start(grid)
    
    first_step = find_first_step(grid, start)
    previous_direction = (-first_step[0], -first_step[1])
    current_position = add_tuples(start, first_step)
    
    while True:
        # FIXME: Need to handle starting position of "S". 
        # At the moment it will just work on the test case by change
        pipe_positions[current_position[0]][current_position[1]] = grid[current_position[0]][current_position[1]]
        
        next_direction = find_next_direction(grid, current_position, previous_direction)
        if next_direction is None: 
            break
        
        previous_direction = (-next_direction[0], -next_direction[1])
        current_position = add_tuples(current_position, next_direction)
        
    total_inside = 0
    is_inside = False
    last_piece: str | None = None
    for row in pipe_positions:
        for item in row:
            
            match item:
                case '|':
                    is_inside = not is_inside
                    last_piece = None
                case 'J':
                    if last_piece == 'L':
                        is_inside = not is_inside
                        
                    last_piece = None
                case '7':
                    if last_piece == 'F':
                        is_inside = not is_inside
                        
                    last_piece = None
                case 'F':
                    is_inside = not is_inside
                    last_piece = 'F'
                case 'L':
                    is_inside = not is_inside
                    last_piece = 'L'
                case '-':
                    continue
                case _:
                    if is_inside and item is None:
                        total_inside += 1
            
    return total_inside
            
            
                
                
            
            
            
                
    
    return total_inside


def find_start(search_grid: list[list[str]]) -> tuple[int, int]:
    for i, line in enumerate(search_grid):
        if START_CHAR not in line:
            continue
        
        return (i, line.index(START_CHAR))
            
    raise ValueError("Start not found??")
    

def find_first_step(grid: list[list[str]], start: tuple[int, int]) -> tuple[int, int]:
    for position in RELATIVE_POSITIONS:
        adjusted_position = add_tuples(start, position)
        
        val = grid[adjusted_position[0]][adjusted_position[1]]
        
        if val == '.':
            continue
        
        match position:
            case (-1, 0):
                if val in ('|', '7', 'F'):
                    return position
            case (1, 0):
                if val in ('|', 'L', 'J'):
                    return position
            case (0, -1):
                if val in ('-', 'L', 'F'):
                    return position
            case (0, 1):
                if val in ('-', 'J', '7'):
                    return position
    
    raise ValueError("No first step found")


def find_next_direction(
    grid: list[list[str]], 
    current_position: tuple[int, int],
    previous_direction: tuple[int, int]
) -> tuple[int, int] | None:
    current_value = grid[current_position[0]][current_position[1]]
    
    match current_value:
        case '|':
            return find_difference([(-1, 0), (1, 0)], previous_direction)
        case '-':
            return find_difference([(0, -1), (0, 1)], previous_direction)
        case 'L':
            return find_difference([(-1, 0), (0, 1)], previous_direction)
        case 'J':
            return find_difference([(-1, 0), (0, -1)], previous_direction)
        case '7':
            return find_difference([(1, 0), (0, -1)], previous_direction)
        case 'F':
            return find_difference([(1, 0), (0, 1)], previous_direction)
        case '.':
            raise ValueError('Reached "." somehow')
        case 'S':
            return
        case _:
            raise ValueError(f'Unrecognised value {current_value}')
        
        
def find_difference(options: list[tuple[int, int]], value: tuple[int, int]):
    return list(set(options).difference(set([value])))[0]

def add_tuples(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return (t1[0] + t2[0], t1[1] + t2[1])
