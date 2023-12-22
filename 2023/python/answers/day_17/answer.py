from itertools import product
from enum import Enum


class Direction(Enum):
    '''Direction of source'''
    UP = (1, 0)
    DOWN = (-1, 0)
    LEFT = (0, 1)
    RIGHT = (0, -1)


Node = tuple[int, int]
Key = tuple[Node, Direction, int]


def part_01(input: str) -> int:
    
    grid = [list(map(int, line)) for line in input.splitlines()]
    height = len(grid)
    width = len(grid[0])
    dimensions = height, width

    start_node = (0, 0)
    start_key = (start_node, Direction.UP, 0)
    final_node = (height - 1, width - 1)
    
    all_keys: set[Key] = set()
    for node in product(range(height), range(width)):
        if node == start_node:
            continue
        for direction in valid_directions(node, dimensions):
            for roll in range(1, valid_crucible_rolls(node, direction, dimensions) + 1):
                all_keys.add((node, direction, roll))
    
    all_keys.add(start_key)    
    open_set: set[Key] = {start_key}
    came_from: dict[Key, Key] = {}
    
    g_score: dict[Key, float] = {start_key: 0}
    f_score: dict[Key, float] = {start_key: h_cost(start_node, final_node)}
    
    while len(open_set) > 0:
        current = closest_key(open_set, g_score)
        
        if current[0] == final_node:
            break
        
        open_set.remove(current)
        
        for neighbor in valid_keys(current):
            if neighbor not in all_keys:
                continue
            
            current_distance = g_score[current]
            cost = grid[neighbor[0][0]][neighbor[0][1]]
            tentative_g_score = current_distance + cost
            
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h_cost(neighbor[0], final_node)
                if neighbor not in open_set:
                    open_set.add(neighbor)
    
    reconstruct_path(came_from, current, dimensions)
      
    return int(min([val for key, val in g_score.items() if key[0] == final_node]))


def part_02(input: str):
    grid = [list(map(int, line)) for line in input.splitlines()]
    height = len(grid)
    width = len(grid[0])
    dimensions = height, width

    start_node = (0, 0)
    start_key = (start_node, Direction.UP, 0)
    final_node = (height - 1, width - 1)
    
    all_keys: set[Key] = set()
    for node in product(range(height), range(width)):
        if node == start_node:
            continue
        for direction in valid_directions(node, dimensions):
            num_rolls = valid_ultra_crucible_rolls(node, direction, dimensions)
            
            if num_rolls < 4:
                continue
            
            for roll in range(4, num_rolls + 1):
                all_keys.add((node, direction, roll))
                
    all_keys.add(start_key)    
    open_set: set[Key] = {start_key}
    came_from: dict[Key, Key] = {}
    
    g_score: dict[Key, float] = {start_key: 0}
    f_score: dict[Key, float] = {start_key: h_cost(start_node, final_node)}
    
    while len(open_set) > 0:
        current = closest_key(open_set, g_score)
        
        if current[0] == final_node:
            break
        
        open_set.remove(current)
        
        for neighbor in valid_ultra_keys(current):
            if neighbor not in all_keys:
                continue
            
            current_distance = g_score[current]
            
            a0, b0 = min(current[0][0], neighbor[0][0]), max(current[0][0], neighbor[0][0]) + 1
            a1, b1 = min(current[0][1], neighbor[0][1]), max(current[0][1], neighbor[0][1]) + 1
            b0 = b0 + 1 if a0 == b0 else b0
            b1 = b1 + 1 if a1 == b1 else b1
            
            cost = sum([sum(row[a1:b1]) for row in grid[a0:b0]]) # FIXME: why does this not match the final path cost?
            tentative_g_score = current_distance + cost
            
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h_cost(neighbor[0], final_node)
                if neighbor not in open_set:
                    open_set.add(neighbor)
                    
    # reconstruct_path(came_from, current, dimensions)
    
    total_path = [current[0]]
    while current in came_from.keys():
        current = came_from[current]
        total_path.insert(0, current[0])
    
    total_cost = 0
    prev_node = total_path[0]
    for node in total_path[1:]:
        
        a0, b0 = min(prev_node[0], node[0]), max(prev_node[0], node[0])
        a1, b1 = min(prev_node[1], node[1]), max(prev_node[1], node[1])
        b0 = b0 + 1 if a0 == b0 else b0
        b1 = b1 + 1 if a1 == b1 else b1
        total_cost += sum(sum(row[a1:b1]) for row in grid[a0:b0])
        prev_node = node
            
    return total_cost - grid[0][0] + grid[height-1][width-1]


def reconstruct_path(came_from: dict[Key, Key], current: Key, dimensions: tuple[int, int]) -> None:
    total_path = [current[0]]
    while current in came_from.keys():
        current = came_from[current]
        total_path.insert(0, current[0])
    
    grid = [['.' for _ in range(dimensions[0])] for _ in range(dimensions[1])]
    for (i, j) in product(range(dimensions[0]), range(dimensions[1])):
        if (i, j) in total_path:
            grid[i][j] = 'X'
            
    for row in grid:
        print(''.join(row))
        


def h_cost(node: Node, end: Node) -> int:
    return abs(node[0] - end[0]) + abs(node[1] - end[1])


def valid_directions(node: Node, dimensions: tuple[int, int]) -> set[Direction]:
    '''Valid directions we could have arrived from'''
    directions: set[Direction] = set()
    height, width = dimensions

    if node[0] - 1 >= 0:
        directions.add(Direction.UP)

    if node[1] - 1 >= 0:
        directions.add(Direction.LEFT)

    if node[0] + 1 < height:
        directions.add(Direction.DOWN)

    if node[1] + 1 < width:
        directions.add(Direction.RIGHT)

    if len(directions) == 0:
        raise ValueError("NO VALID NEIGHBOURS FOUND")

    return directions


def valid_crucible_rolls(node: Node, direction: Direction, dimensions: tuple[int, int]) -> int:
    '''Returns the number of valid rolls in a certain direction. Can only be of max 3'''
    height, width = dimensions
    
    match direction:
        case Direction.UP:
            return min(node[0], 3)
        case Direction.LEFT:
            return min(node[1], 3)
        case Direction.DOWN:
            return min(height - node[0] - 1, 3)
        case Direction.RIGHT:
            return min(width - node[1] - 1, 3)
        
        
def valid_ultra_crucible_rolls(node: Node, direction: Direction, dimensions: tuple[int, int]) -> int:
    '''Returns the number of valid rolls in a certain direction. Can be of max 10'''
    height, width = dimensions
    
    match direction:
        case Direction.UP:
            return min(node[0], 10)
        case Direction.LEFT:
            return min(node[1], 10)
        case Direction.DOWN:
            return min(height - node[0] - 1, 10)
        case Direction.RIGHT:
            return min(width - node[1] - 1, 10)


def closest_key(open_set: set[Key], distances: dict[Key, float]) -> Key:
    open_distances = {key: distances[key] for key in open_set}
    return sorted(open_distances.items(), key=lambda x: x[1])[0][0]


def valid_keys(key: Key) -> list[Key]:
    node, direction, moves = key

    if node == (0, 0):
        return [
            ((0, 1), Direction.LEFT, 1),
            ((1, 0), Direction.UP, 1),
        ]

    keys: list[Key] = []

    # Case: moves is less than 3 -> Can continue on in same dir at least 1 more time
    if moves < 3:
        new_node = (
            node[0] + direction.value[0], 
            node[1] + direction.value[1],
        )

        keys.append((new_node, direction, moves + 1))
    
    # Case: the 90 degree turns
    match direction:
        case Direction.UP | Direction.DOWN:
            for d in [Direction.LEFT, Direction.RIGHT]:
                new_node = (
                    node[0] + d.value[0],
                    node[1] + d.value[1],
                )

                keys.append((new_node, d, 1))
        case Direction.LEFT | Direction.RIGHT:
            for d in [Direction.UP, Direction.DOWN]:
                new_node = (
                    node[0] + d.value[0],
                    node[1] + d.value[1],
                )

                keys.append((new_node, d, 1))

    return keys


def valid_ultra_keys(key: Key) -> list[Key]:
    node, direction, moves = key

    if node == (0, 0):
        return [
            ((0, 4), Direction.LEFT, 4),
            ((4, 0), Direction.UP, 4),
        ]

    keys: list[Key] = []

    if moves < 10:
        new_node = (
            node[0] + direction.value[0], 
            node[1] + direction.value[1],
        )

        keys.append((new_node, direction, moves + 1))
    
    # Case: the 90 degree turns
    match direction:
        case Direction.UP | Direction.DOWN:
            for d in [Direction.LEFT, Direction.RIGHT]:
                new_node = (
                    node[0] + (d.value[0] * 4),
                    node[1] + (d.value[1] * 4),
                )

                keys.append((new_node, d, 4))
        case Direction.LEFT | Direction.RIGHT:
            for d in [Direction.UP, Direction.DOWN]:
                new_node = (
                    node[0] + (d.value[0] * 4),
                    node[1] + (d.value[1] * 4),
                )

                keys.append((new_node, d, 4))

    return keys
