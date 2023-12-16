def part_01(input: str) -> int:
    grid = [list(line) for line in input.splitlines()]
    total_weight = 0
    
    
    for column in [list(x) for x in zip(*grid)]:
        column = roll_rocks(column)
        max_distance = len(column)
        rock_distances = [max_distance - i for i, rock in enumerate(column) if rock == 'O']
        total_weight += sum(rock_distances)
        
    return total_weight


def part_02(input: str) -> int:
    grid = [list(line) for line in input.splitlines()]
    
    for n in range(1, 100000):
        # Roll north
        new_grid: list[list[str]] = []
        for column in [list(x) for x in zip(*grid)]:
            new_grid.append(roll_rocks(column))
        # Untranspose
        grid = [list(x) for x in zip(*new_grid)]
        
        # print_grid(grid, rotations=(n % 4))
        
        if n % 4 == 0:
            rotated_grid = grid[:]
            for _ in range(3):
                rotated_grid = [list(x) for x in zip(*grid[::-1])]
            
            total_weight = 0
            for column in [list(x) for x in zip(*rotated_grid)]:
                max_distance = len(column)
                rock_distances = [max_distance - i for i, rock in enumerate(column) if rock == 'O']
                total_weight += sum(rock_distances)
                
            print(f'Cycle: {int(n / 4)} = {total_weight}')
        
        # Rotate next
        grid = [list(x) for x in zip(*grid[::-1])]
        
    '''
    Cycle length == 9
    round(1000000000 / 9) = 111111111
    1000000000 - 111111111 * 9 = 1
    Answer will be at cycle # % 9 = 1
    Manually found result = 96317
    TODO: Actually automate this part
    '''
    
    raise NotImplementedError
    

def roll_rocks(column: list[str]) -> list[str]:
    '''This rolls rocks fron right to left in a column'''
    for i, val in enumerate(column):
        if i == 0:
            continue
        
        is_unmovable = val in ['.', '#']
        if is_unmovable:
            continue
        
        is_blocked = column[i - 1] in ['O', '#']
        if is_blocked:
            continue
        
        for j in reversed(range(i)):
            next_is_free = column[j] == '.'
            
            if j == 0 and column[0] == '.':
                column[j] = 'O'
                column[i] = '.'    
                break
            
            if next_is_free:
                continue
            
            column[j + 1] = 'O'
            column[i] = '.'
            break
    
    return column


def print_grid(grid: list[list[str]], rotations: int = 0) -> None:
    for _ in range(3 + rotations):
        grid = [list(x) for x in zip(*grid)][::-1]
    
    for row in grid:
        print(''.join(row))
        
    print()