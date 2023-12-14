def part_01(input: str) -> int:
    blocks = [block.splitlines() for block in input.split('\n\n')]
    total = 0

    for block in blocks:
        horizontal_reflection = find_mirror_index(block, 0) 
        vertical_reflection = find_mirror_index(reverse_block(block), 0)
        print(horizontal_reflection, vertical_reflection)

        if horizontal_reflection is not None:
            total += 100 * horizontal_reflection

        if vertical_reflection is not None:
            total += vertical_reflection

    return total

def part_02(input: str) -> int:
    blocks = [block.splitlines() for block in input.split('\n\n')]
    total = 0

    for block in blocks:
        old_reflections = (find_mirror_index(block, 0), find_mirror_index(reverse_block(block), 0))

        original_block = block[:]
        unique_reflections = {old_reflections}
        for i in range(len(block[0])):
            for j in range(len(block)):
                block = [list(row) for row in block]
                block[j][i] = '#' if block[j][i] == '.' else '#'
                block = [''.join(row) for row in block]
                new_reflections = (
                    find_mirror_index(block, 0, old_reflections[0]), 
                    find_mirror_index(reverse_block(block), 0, old_reflections[1])
                )
                block = original_block[:]
                unique_reflections.add(new_reflections)
                
        new_reflections =([
            reflection for reflection in unique_reflections 
            if reflection != old_reflections and reflection != (None, None)
        ])[0]

        if new_reflections[0] is not None:
            total += 100 * new_reflections[0]

        if new_reflections[1] is not None:
            total += new_reflections[1]
       
    return total


def find_mirror_index(
    block: list[str], 
    num_smudges: int = 0, 
    skip_row: int | None = None
) -> int | None:
    # FIXME: Revert back to using num_smudges instead of brute force

    prev_row = ''

    for i, row in enumerate(block):
        num_differences = sum(1 for a, b in zip(prev_row, row) if a != b)
        if num_differences <= num_smudges and i > 0:
            num_smudges -= num_differences

            if i == 1 and i != skip_row:
                return 1

            max_range = min(i - 1, len(block) - (i + 1))
            break_loop = False
            for j in range(1, max_range + 1):
                num_differences = sum(1 for a, b in zip(block[i - (1 + j)], block[i + j]) if a != b)
                if num_differences > num_smudges:
                    break_loop = True
                else:
                    num_smudges -= num_differences

            if not break_loop and i != skip_row:
                return i

        prev_row = row

    return None


def reverse_block(block: list[str]) -> list[str]:
    reversed_block = []
    for n in range(len(block[0])):
        reversed_block.append(''.join([line[n] for line in block]))

    return reversed_block

