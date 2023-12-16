def part_01(input: str) -> int:
    codes = input.split(',')
    return sum([hash_algorithm(code) for code in codes])


def part_02(input: str) -> str:
    return "Part two answer"


def hash_algorithm(code: str) -> int:
    total = 0
    ascii_vals = [ord(char) for char in code]
    
    for val in ascii_vals:
        total += val
        total *= 17
        total %= 256

    return total