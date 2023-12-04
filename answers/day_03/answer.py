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
                
                
                
                    

                
            
            # Need to somehow skip the whole number when first digit processed
            
    
    return schematic

def part_02(input: str) -> str:
    return "Part two answer"
