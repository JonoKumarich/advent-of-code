def part_01(input: str) -> int:
    blocks = [block.splitlines() for block in input.split('\n\n')]
    total = 0

    for block in blocks:
        horizontal_reflection = find_mirror_index(block, 0) 
        vertical_reflection = find_mirror_index(reverse_block(block), 0)
        total += 100 * horizontal_reflection
        total += vertical_reflection
    return total

def part_02(input: str) -> int:
    blocks = [block.splitlines() for block in input.split('\n\n')]
    total = 0

    for block in blocks:
        horizontal_reflection = find_mirror_index(block, 1) 
        vertical_reflection = find_mirror_index(reverse_block(block), 1)
        # TODO: Return correct value of the two as both can be non-zero
        # TODO: Handle case when both values equal. Let's assume that the smudge case would be better
        # We need to cause a different reflection line for each one
        print(blocks.index(block), horizontal_reflection, vertical_reflection, find_mirror_index(block), find_mirror_index(reverse_block(block)))
    return total

def find_mirror_index(block: list[str], num_smudges: int = 0) -> int:

    prev_row = ''

    for i, row in enumerate(block):
        num_differences = sum(1 for a, b in zip(prev_row, row) if a != b)
        if num_differences <= num_smudges and i > 0:
            num_smudges -= num_differences

            if i == 1:
                return 1

            max_range = min(i - 1, len(block) - (i + 1))
            break_loop = False
            for j in range(1, max_range + 1):
                num_differences = sum(1 for a, b in zip(block[i - (1 + j)], block[i + j]) if a != b)
                if num_differences > num_smudges:
                    break_loop = True
                else:
                    num_smudges -= num_differences

            if not break_loop:
                return i

        prev_row = row

    return 0


def reverse_block(block: list[str]) -> list[str]:
    reversed_block = []
    for n in range(len(block[0])):
        reversed_block.append(''.join([line[n] for line in block]))

    return reversed_block

