from itertools import combinations


def part_01(input: str) -> int:
    grid = [list(line) for line in input.splitlines()]
    
    universe = expand_universe_vertically(grid)
    universe = [list(x) for x  in zip(*universe)] # invert
    universe = expand_universe_vertically(universe)
    universe = [list(x) for x  in zip(*universe)] # un-invert

    galaxies: list[tuple[int, int]] = []
    for r, row in enumerate(universe):
        for c, val in enumerate(row):
            if val == '#':
                galaxies.append((r, c))
        
    total = 0
    for a, b in combinations(galaxies, 2):
        total += manhattan(a, b)
        
    return total
        
    
def part_02(input: str) -> int:
    """
    Steps:
        - Do not expant universe
        - Get indexes in which contain no galaxies
        - For each point:
            - calculate manhatten distance
            - calculate number of times it crosses these indexes
                - add # indexes x expansion multiplier and add to manhatten distance
    """
    
    grid = [list(line) for line in input.splitlines()]
    
    clear_horizontal: list[int] = []
    for i in range(len(grid)):
        if all([val == '.' for val in grid[i]]):
            clear_horizontal.append(i)
    
    clear_vertical: list[int] = []
    for i in range(len(grid[0])):
        if all ([row[i] == '.' for row in grid]):
            clear_vertical.append(i)
    
    galaxies: list[tuple[int, int]] = []
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == '#':
                galaxies.append((r, c))
    
    total = 0
    for a, b in combinations(galaxies, 2):
        MULTIPLIER = 1000000 - 1
        total += len([val for val in clear_horizontal if val > min(a[0], b[0]) and val < max(a[0], b[0])]) * MULTIPLIER
        total += len([val for val in clear_vertical if val > min(a[1], b[1]) and val < max(a[1], b[1])]) * MULTIPLIER
        
        total += manhattan(a, b)
    
    
    return total


def expand_universe_vertically(universe: list[list[str]]) -> list[list[str]]:
    clear_horizontal: list[int] = []
    for i in range(len(universe)):
        if all([val == '.' for val in universe[i]]):
            clear_horizontal.append(i)
            
    moved_tally = 0
    for i in clear_horizontal:
        universe.insert(i + moved_tally, universe[i + moved_tally])
        moved_tally += 1

    return universe
    
    
def manhattan(a: tuple[int, int], b: tuple[int, int]):
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))