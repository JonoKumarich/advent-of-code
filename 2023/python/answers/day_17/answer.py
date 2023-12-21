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
    final_node = (height - 1, width - 1)
    
    distances: dict[Key, float] = {}
    for node in product(range(height), range(width)):
        if node == start_node:
            continue
        for direction in valid_directions(node, dimensions):
            for roll in range(1, valid_rolls(node, direction, dimensions) + 1):
                distances[(node, direction, roll)] = float('inf')
    
    distances[(start_node, None, 0)] = 0
    unvisited: set[Key] = set(distances.keys())

    while len(unvisited) > 0:
        key = closest_key(unvisited, distances)

        if key[0] == final_node:
            break
        
        print(key)

        unvisited.remove(key)
        for next_key in valid_keys(key, unvisited):
            potential_distance = distances[key] + grid[next_key[0][0]][next_key[0][1]]
            
            if potential_distance < distances[next_key]:
                distances[next_key] = potential_distance
                
    return distances[key]


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


def closest_key(unvisited: set[Key], distances: dict[Key, float]) -> Key:
    # FIXME: This is a bottleneck
    unvisited_distances = {k: v for (k, v) in distances.items() if k in unvisited}
    return sorted(unvisited_distances.items(), key=lambda item: item[1])[0][0]


def valid_keys(key: Key, distance_keys: set[Key]) -> list[Key]:
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

    return [key for key in keys if key in distance_keys]








