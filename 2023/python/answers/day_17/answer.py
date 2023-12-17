from itertools import product


def part_01(input: str) -> int:
    grid = parse_grid(input)
        
    unvisited_nodes = {(i, j) for (i, j) in product(range(len(grid)), range(len(grid[0])))}
    distances = {node: float('inf') for node in unvisited_nodes}
    distances[(0, 0)] = 0
    
    destination_node = (len(grid) - 1, len(grid[0]) - 1)
    current_node = (0, 0)
    previous_node: tuple[int, int] | None = None
    straight_rolls = 1
    
    while True:
        neighbours = find_neighbours(current_node, previous_node, straight_rolls)
        neighbours = filter_neighbour_bounds(neighbours, grid)
        
        current_node_distance = distances[current_node]
        
        min_val = float('inf')
        best_next_node = None
        for next_node in neighbours:
            if next_node not in unvisited_nodes:
                continue
            
            tentative_distance = current_node_distance + grid[next_node[0]][next_node[1]]
            distances[next_node] = min(distances[next_node], tentative_distance) if next_node in distances else tentative_distance
            
            if tentative_distance < min_val:
                best_next_node = next_node
                min_val = tentative_distance

        unvisited_nodes.remove(current_node)
        
        if destination_node not in unvisited_nodes:
            break
        
        if best_next_node is None:
            raise ValueError('No best next node???')
        
        # ERROR: How does current node and next best node become equal?????
        straight_rolls = 1 if is_path_corner(best_next_node, previous_node) else straight_rolls + 1
        previous_node = current_node
        
    
    return int(distances[destination_node])
                


def part_02(input: str) -> str:
    return "Part two answer"


def parse_grid(input: str) -> list[list[int]]:
    return [list(map(int, line)) for line in input.splitlines()]


def find_neighbours(
    node: tuple[int, int], 
    previous_node: tuple[int, int] | None,
    num_straight_rolls: int
) -> set[tuple[int, int]]:
    
    neighbours = {
        (node[0] + 1, node[1]),
        (node[0] - 1, node[1]),
        (node[0], node[1] + 1),
        (node[0], node[1] - 1),
    }
    
    if previous_node is None:
        return neighbours
    
    print(previous_node, neighbours)
    assert previous_node in neighbours
    
    # Can only roll 3 times in a row forward
    if num_straight_rolls == 3:
        diff = (node[0] - previous_node[0], node[1] - previous_node[1])
        neighbours.remove((node[0] + diff[0], node[1] + diff[1]))
    
    # Can not rotate 180 degrees    
    neighbours.remove(previous_node)
        
    return neighbours


def filter_neighbour_bounds(neighbours: set[tuple[int, int]], grid: list[list[int]]) -> set[tuple[int, int]]:
    valid_neighbours: set[tuple[int, int]] = set()
    
    for neighbour in neighbours:
        is_below = min(neighbour[0], neighbour[1]) < 0
        is_lower = neighbour[0] >= len(grid)
        is_right = neighbour[1] >= len(grid[0])
        
        if not (is_below or is_lower or is_right):
            valid_neighbours.add(neighbour)
    
    return valid_neighbours


def is_path_corner(next_node: tuple[int, int], previous_node: tuple[int, int] | None) -> bool:
    
    if previous_node is None:
        return True
    
    return max(
        abs(next_node[0] - previous_node[0]),
        abs(next_node[1] - previous_node[1])
    ) == 1