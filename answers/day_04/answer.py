def part_01(input: str) -> str:
    lines = input.splitlines()
    total = 0
    
    for line in lines:
        winning_numbers, our_numbers = line.split(': ')[1].split(' | ')
        winning_numbers = [int(num) for num in winning_numbers.split(' ') if num !=  '']
        our_numbers = [int(num) for num in our_numbers.split(' ') if num !=  '']
        matches = [x for x in winning_numbers if x in our_numbers]
        
        num_matches = len(matches)
        
        if num_matches == 0:
            continue
        
        total += 2**(num_matches-1)
        
    return total


def part_02(input: str) -> str:
    return "Part two answer"
