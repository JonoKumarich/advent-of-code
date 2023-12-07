import re

NUM_REGEX = r"[^0-9]"
TEXT_NUM_REGEX = r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))"

def part_01(input: str) -> str:
    numbers = [re.sub(NUM_REGEX, "", line) for line in input.splitlines()]
    return sum(join_first_and_last_digits(digits) for digits in numbers)

def part_02(input: str) -> str:
    
    digit_lines = [
        [get_digit(digit) for digit in re.findall(TEXT_NUM_REGEX, line)] 
        for line in input.splitlines()
    ]
    
    return sum(join_first_and_last_digits(digits) for digits in digit_lines)
    

def get_digit(number_text: str) -> int:
    '''Converts numbers to integers from both str and English text form.'''
    try:
        return {
            'one': 1, 
            'two': 2, 
            'three': 3, 
            'four': 4, 
            'five': 5, 
            'six': 6, 
            'seven': 7, 
            'eight': 8, 
            'nine': 9,
        }[number_text]
    except KeyError:
        return int(number_text)


def join_first_and_last_digits(digits: list[int]) -> int:
    '''Joins first and last digits together into an integer'''
    joined_string = str(digits[0]) + str(digits[-1])
    return int(joined_string)
    