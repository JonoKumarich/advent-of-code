def part_01(input: str) -> int:
    total_weight = 0

    for column in parse_input(input):
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
                # J = next spot, J - 1 = current spot
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
        
        max_distance = len(column)
        rock_distances = [max_distance - i for i, rock in enumerate(column) if rock == 'O']
        total_weight += sum(rock_distances)
        
    return total_weight

def part_02(input: str) -> int:
    return 0


def parse_input(input: str) -> list[list[str]]:
    vertical = [list(line) for line in input.splitlines()]
    return [list(x) for x in zip(*vertical)] 
