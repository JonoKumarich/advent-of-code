MAX_COLORS = {
    'red': 12,
    'green': 13,
    'blue': 14
}


def part_01(input: str) -> str:
    lines = [line.split(': ') for line in input.splitlines()]
    games = {game[0].split(' ')[1]: game[1].split('; ') for game in lines}
    
    total_ids = 0
    
    for game in games:
        
        game_is_valid = True
        
        for round in games[game]:            
            for color in round.split(', '):
                number, color_value = color.split(' ')
                
                if int(number) > MAX_COLORS[color_value]:
                    game_is_valid = False
                
        if game_is_valid:
            total_ids += int(game)
            
            
    return total_ids


def part_02(input: str) -> str:
    return "Part two answer"
