DIRECTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}


def part_01(input: str) -> int:
    lines = [line.split() for line in input.splitlines()]
    current_position = (0, 0)
    corners = [(0, 0)]
    
    # Generate corners
    for direction, num, _ in lines:
        next_dir = DIRECTIONS[direction]
        next_position = (
            current_position[0] + (next_dir[0] * int(num)),
            current_position[1] + (next_dir[1] * int(num))
        )
        corners.append(next_position)
        current_position = next_position
    
    offsets = (min(val[0] for val in corners), min(val[1] for val in corners))
    # Adjust to make true grid index corners
    corners = [(corner[0] - offsets[0], corner[1] - offsets[1]) for corner in corners]

    height = max(val[0] for val in corners) + 1
    width = max(val[1] for val in corners) + 1

    full_edges: list[tuple[int, int]] = []
    full_edges.extend(corners)
    # Generate edges
    last_corner = corners[0]
    for corner in corners[1:]:
        if last_corner[1] == corner[1]:
            for a in range(min(last_corner[0], corner[0]) + 1, max(last_corner[0], corner[0])):
                full_edges.append((a, corner[1]))

        if last_corner[0] == corner[0]:
            for b in range(min(last_corner[1], corner[1]) + 1, max(last_corner[1], corner[1])):
                full_edges.append((corner[0], b))

        last_corner = corner

    node_values: dict[tuple[int, int], str] = {}
    for node in full_edges:
        if (node[0] - 1, node[1]) in full_edges and (node[0] + 1, node[1]) in full_edges:
            node_values[node] = '|'
        elif (node[0], node[1] - 1) in full_edges and (node[0], node[1] + 1) in full_edges:
            node_values[node] = '-'
        elif (node[0] - 1, node[1]) in full_edges:
            if (node[0], node[1] - 1) in full_edges:
                node_values[node] = 'J'
            elif (node[0], node[1] + 1) in full_edges:
                node_values[node] = 'L'
            else:
                raise ValueError(node)
        elif (node[0] + 1, node[1]) in full_edges:
            if (node[0], node[1] - 1) in full_edges:
                node_values[node] = '7'
            elif (node[0], node[1] + 1) in full_edges:
                node_values[node] = 'F'
            else:
                raise ValueError(node)
        else:
            raise ValueError(node)
        
    grid: list[list[str | None]] = [[None] * width for _ in range(height)]
    for pos in full_edges:
        grid[pos[0]][pos[1]] = node_values[(pos[0], pos[1])]
        
    total_inside = 0
    is_inside = False
    last_piece: str | None = None
    for row in grid:
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
            
    return total_inside + len(full_edges) - 1

    
    

def part_02(input: str) -> str:
    return "Part two answer"
