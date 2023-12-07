
def amount_of_winning_numbers(scratch_card: str) -> int:
    winning_numbers, our_numbers = scratch_card.split(': ')[1].split(' | ')
    winning_numbers = [int(num) for num in winning_numbers.split(' ') if num !=  '']
    our_numbers = [int(num) for num in our_numbers.split(' ') if num !=  '']
    matches = [x for x in winning_numbers if x in our_numbers]
    return len(matches)


def part_01(input: str) -> str:
    lines = input.splitlines()
    total = 0
    
    for line in lines:
        num_matches = amount_of_winning_numbers(line)

        if num_matches == 0:
            continue
        
        total += 2**(num_matches-1)
        
    return total


def part_02(input: str) -> str:
    lines = input.splitlines()
    numbers_of_cards = {line.split(': ')[0][5:].strip(): 1 for line in lines}
    
    for line in lines:
        card_number = int(line.split(': ')[0][5:].strip())
        quantity = numbers_of_cards[str(card_number)]
        matches = amount_of_winning_numbers(line)
        
        for i in range(1, matches+1):
            numbers_of_cards[str(card_number + i)] = numbers_of_cards[str(card_number + i)] + quantity
    
    return sum(numbers_of_cards.values())
