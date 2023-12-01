import re

def part_01(input: str) -> str:
    numbers = [re.sub("[^0-9]", "", line) for line in input.splitlines()]
    total = 0
    
    for line in numbers:
        total += int(line[0] + line[-1])
        
    return str(total)

def part_02(input: str) -> str:
    # Assumption that no duplicates. If doesn't work, then lets fix. --> NEED TO FIX THIS
    
    numbers = {
        'one': 1, 
        'two': 2, 
        'three': 3, 
        'four': 4, 
        'five': 5, 
        'six': 6, 
        'seven': 7, 
        'eight': 8, 
        'nine': 9,
        '1': 1, 
        '2': 2, 
        '3': 3, 
        '4': 4, 
        '5': 5, 
        '6': 6, 
        '7': 7, 
        '8': 8, 
        '9': 9
    }
    
    total = 0
    
    for line in input.splitlines():
        first_occurance = {number: line.find(number) for number in numbers if line.find(number) != -1}
        last_occurance = {number: line.rfind(number) for number in numbers if line.find(number) != -1}
        
        first_number = numbers[sorted(first_occurance.items(), key=lambda x:x[1])[0][0]]
        last_number = numbers[list(reversed(sorted(last_occurance.items(), key=lambda x:x[1])))[0][0]] 
        
        
        final_number = str(first_number) + str(last_number)
        print(final_number)
        total += int(final_number)
        
        
    return str(total)
