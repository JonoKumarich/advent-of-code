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
            for roll in range(1, valid_rolls(node, direction, dimensions) + 1):
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
            
    return int(min([val for key, val in g_score.items() if key[0] == final_node]))


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


def valid_rolls(node: Node, direction: Direction, dimensions: tuple[int, int]) -> int:
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








