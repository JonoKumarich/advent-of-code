CHARS = ['+', '&', '/', '$', '@', '%', '*', '=', '#', '-']

def part_01(input: str) -> str:
    schematic = [list(line) for line in input.splitlines()]
    total_part_numbers = 0
    
    n_rows = len(schematic)
    n_cols = len(schematic[0])
    
    for i in range(n_rows):
        checked_js = []
        
        for j in range(n_cols):
            if j in checked_js:
                continue
            
            # If digit found, calculate length of chars in number
            digit_found = schematic[i][j].isdigit()
            if digit_found:
                number_length = 1
                
                while True:  
                    if j + number_length >= n_cols:
                        break
                      
                    if not schematic[i][j+number_length].isdigit():
                        break
                    
                    number_length += 1
            
                # Check adjacent cells for a symbol.
                symbols_found = []
                row_range = max(i-1, 0), min(i+2, n_rows)
                col_range = max(j-1, 0), min(j+number_length+1, n_cols)
                
                for row in schematic[row_range[0]:row_range[1]]:
                    symbols_found.extend(row[col_range[0]:col_range[1]])

                unique_symbols = set(symbols_found)
                
                # Add numbers to total if adjacent cell contains symbol
                if len([value for value in unique_symbols if value in CHARS]) > 0:
                    total_part_numbers += int(''.join(schematic[i][j:j+number_length]))
                    
                checked_js.extend(list(range(j,j+number_length)))
                
    return total_part_numbers


def part_02(input: str) -> str:
    '''
    Assumptions: Only ever 2 numbers surrounding a gear
    
    Locate all potential gear indices
    For each gear index, locate surrounding numbers
    Count:
        Num vals above
        Num vals below
        Num vals left
        Num vals right
    If 2 categories have vals, then collect numbers based on location
    If just top or bottom, then check if numbers are connected or separate
    '''
    
    # Answer has too much duplication in walk left / right logic. Let's clean that up in the future.
    
    schematic = [list(line) for line in input.splitlines()]
    total = 0
    
    # Get gear locations
    star_locations = [[(i, j) for j, val in enumerate(row) if val == "*"] for i, row in enumerate(schematic)]
    potential_gears = []
    for row in star_locations:
        potential_gears.extend(row)
    
    for gear in potential_gears:
        
        neighbours = []
        neighbours.extend(get_row_numbers(schematic, gear, -1)) # Top row
        neighbours.extend(get_row_numbers(schematic, gear, 1)) # Bottom row
        
        # Walk right
        if schematic[gear[0]][gear[1]-1].isdigit():
            number = ''
            
            left_index = gear[1] - 1
            while True:
                if left_index < 0:
                    break
                
                val = schematic[gear[0]][left_index]
                
                if not val.isdigit():
                    break 
                
                number = val + number
                left_index -= 1
                
            neighbours.append(number)
        
        # Walk right
        if schematic[gear[0]][gear[1]+1].isdigit():
            number = ''
            
            right_index = gear[1] + 1
            while True:
                if right_index > len(schematic[0]) - 1:
                    break
                
                val = schematic[gear[0]][right_index]
                
                if not val.isdigit():
                    break 
                
                number = number + val
                right_index += 1
                
            neighbours.append(number)
        
        print(gear, neighbours)
        if len(neighbours) == 2:
            total += int(neighbours[0]) * int(neighbours[1])
        
    return total


def get_row_numbers(schematic: list[list[str]], gear: tuple[int, int], offset: int) -> list[int]:
    
    if offset not in [-1, 1]:
        raise ValueError(f"Invalid offset {offset}")
    
    is_top = gear[0] == 0
    is_bottom = gear[0] == len(schematic) - 1
    
    if (offset == -1 and is_top) or (offset == 1 and is_bottom):
        return []
    
    left, middle, right = schematic[gear[0]+offset][gear[1]-1:gear[1]+2]
    
    if not any([left.isdigit(), middle.isdigit(), right.isdigit()]):
        return []
    
    # If middle then walk both ways - can return
    if middle.isdigit():
        number = middle
        
        
        # Walk right
        right_index = gear[1] + 1
        while True:
            if right_index > len(schematic[0]) - 1:
                break
            
            val = schematic[gear[0]+offset][right_index]
            
            if not val.isdigit():
                break 
            
            number = number + val
            right_index += 1
        
        # Walk left
        left_index = gear[1] - 1
        while True:
            if left_index < 0:
                break
            
            val = schematic[gear[0]+offset][left_index]
            
            if not val.isdigit():
                break 
            
            number = val + number
            left_index -= 1
            
        return [number]
    
    numbers = []
    
    # If left, then walk left
    if left.isdigit():
        number = ''
        left_index = gear[1] - 1

        while True:
            if left_index < 0:
                break
            
            val = schematic[gear[0]+offset][left_index]

            if not val.isdigit():
                break 
            
            number = val + number
            left_index -= 1
        
        numbers.append(number)
        
    # If right, then walk right
    if right.isdigit():
        number = ''
        right_index = gear[1] + 1
        while True:
            if right_index > len(schematic[0]) - 1:
                break
            
            val = schematic[gear[0]+offset][right_index]
            
            if not val.isdigit():
                break 
            
            number = number + val
            right_index += 1
        
        numbers.append(number)
    
    return numbers
