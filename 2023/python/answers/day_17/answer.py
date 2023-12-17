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
            potential_distance = distances[node] + grid[next_node[0]][next_node[1]]
            
            if potential_distance < distances[next_node]:
                distances[next_node] = potential_distance
                
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
    