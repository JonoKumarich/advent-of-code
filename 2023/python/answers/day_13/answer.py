def part_01(input: str) -> int:
    # ERROR: Maybe it is not scanning the last row/col?
    blocks = [block.splitlines() for block in input.split('\n\n')]
    total = 0
    for block in blocks:
        total += 100 * find_mirror_index(block)
        total += find_mirror_index(reverse_block(block))

    return total

def part_02(input: str) -> int:
    return 1

def find_mirror_index(block: list[str]) -> int:

    prev_row = ''
    for i, row in enumerate(block):

        if prev_row == row:
            if i == 1:
                return 1

            max_range = min(i - 1, len(block) - (i + 1))
            break_loop = False
            for j in range(1, max_range + 1):
                if block[i - (1 + j)] != block[i + j]:
                   break_loop = True 

            if not break_loop:
                return i

        prev_row = row

    return 0

def reverse_block(block: list[str]) -> list[str]:
    reversed_block = []
    for n in range(len(block[0])):
        reversed_block.append(''.join([line[n] for line in block]))

    return reversed_block

