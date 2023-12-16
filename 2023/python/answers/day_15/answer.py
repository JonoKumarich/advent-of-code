import re


CODE_REGEX = r"([a-zA-Z]+)([=-])(\d*)"


def part_01(input: str) -> int:
    codes = input.split(',')
    return sum([hash_algorithm(code) for code in codes])


def part_02(input: str) -> int:
    steps = [re.findall(CODE_REGEX, step)[0] for step in input.split(',')]
    boxes: dict[int, list[tuple[str, int]]] = {}

    for code, op, num in steps:
        box = hash_algorithm(code)
        
        match op:
            case '=':
                if box not in boxes.keys():
                    boxes[box] = [(code, int(num))]
                
                labels = [label for label, _ in boxes[box]]
                
                if code in labels:
                    boxes[box][labels.index(code)] = (code, int(num))
                else:
                    boxes[box].append((code, int(num)))
            case '-':
                if box not in boxes.keys():
                    continue
                
                boxes[box] = [(label, lens) for label, lens in boxes[box] if label != code]
            case _:
                raise ValueError(f'Value: {op} not handled')
        
    total = 0
    for num, box in boxes.items():
        for i, (_, lens) in enumerate(box):
            total += (num + 1) * (i + 1) * lens
    
    return total


def hash_algorithm(code: str) -> int:
    total = 0
    ascii_vals = [ord(char) for char in code]
    
    for val in ascii_vals:
        total += val
        total *= 17
        total %= 256

    return total