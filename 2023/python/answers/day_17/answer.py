from itertools import product

Node = tuple[int, int]

def part_01(input: str) -> int:
    
    grid = [list(map(int, line)) for line in input.splitlines()]
    height = len(grid)
    width = len(grid[0])
    
    distances = {
        (i, j): float('inf') 
        for (i, j) in product(range(height), range(width))
    }
    
    roll_history: dict[Node, list[Node]] = {
        (i, j): []
        for (i, j) in product(range(height), range(width))
    }
    
    node = (0, 0)
    final_node = (height - 1, width - 1)
    distances[node] = 0
    
    unvisited = set(distances.keys())
    
    while len(unvisited) > 0:
        node = get_closest_node(unvisited, distances)
        
        if node == final_node:
            break
        
        unvisited.remove(node)
        
        for next_node in find_neighbouring_nodes(node, (height, width)):
            # # Can't go back on itself
            # if next_node == roll_history[node][-1]:
            #     continue
            
            if is_more_than_three_rolls(roll_history[node][-3:], next_node):
                continue
            
            potential_distance = distances[node] + grid[next_node[0]][next_node[1]]
            
            if potential_distance < distances[next_node]:
                roll_history[next_node] = roll_history[node] + [node]
                distances[next_node] = potential_distance
                
    print_grid = [[str(val) for val in row] for row in grid]
    
    for roll in roll_history[(12, 12)]:
        print_grid[roll[0]][roll[1]] = ' '
        
    for row in print_grid:
        print(''.join(row))
        
    return int(distances[(height - 1, width - 1)])

            
def get_closest_node(unvisited: set[Node], distances: dict[Node, float]) -> Node:
    unvisited_distances = {k: v for (k, v) in distances.items() if k in unvisited}
    return sorted(unvisited_distances.items(), key=lambda item: item[1])[0][0]
            
    
def find_neighbouring_nodes(
    node: Node, 
    max_dimensions: tuple[int, int]
) -> set[Node]:
    
    neighbouring_nodes = {
        (node[0] - 1, node[1]),
        (node[0] + 1, node[1]),
        (node[0], node[1] - 1),
        (node[0], node[1] + 1),    
    }
    
    filtered_nodes: set[Node] = set()
    for node in neighbouring_nodes:
        if min(node[0], node[1]) >= 0 and node[0] < max_dimensions[0] and node[1] < max_dimensions[1]:
            filtered_nodes.add(node)
    
    return filtered_nodes
    
    
def is_more_than_three_rolls(roll_history: list[Node], next_roll: Node) -> bool:
    all_rolls = roll_history + [next_roll]
    heights = [roll[0] for roll in all_rolls]
    widths = [roll[1] for roll in all_rolls]
    
    if max(heights) - min(heights) >= 4:
        return True
    
    if max(widths) - min(widths) >= 4:
        return True
    
    return False


# def dijkstra(grid: list[list[int]], starting_position: Node, roll_history: dict[Node, list[Node]]) -> int:
    