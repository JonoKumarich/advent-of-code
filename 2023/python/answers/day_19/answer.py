import re


PARTS = ['x', 'm', 'a', 's']


def part_01(input: str) -> int:
    split_input = parse_input(input)

    workflows = {
        workflow[0]: (workflow[1], workflow[2]) 
        for workflow in (parse_workflow(w) for w in split_input[0])
    }
    
    ratings = parse_ratings(split_input[1])
    rating_results: dict[int, str] = {}
    
    for n, rating in enumerate(ratings):
        workflow = workflows['in']
        
        to_break = False
        while not to_break:
            
            for part, op, threshold, next in workflow[0]:
                value = rating[part]
                
                if not threshold_success(op, threshold, value):
                    continue
                
                if next in ['A', 'R']:
                    rating_results[n] = next
                    to_break = True
                    break
                
                workflow = workflows[next]
                break
                
                    
            if to_break:    
                continue
                
            if workflow[1] in ['A', 'R']:
                rating_results[n] = workflow[1]
                break
            
            workflow = workflows[workflow[1]]
    
    accepted_ratigns = [key for (key, value) in rating_results.items() if value == 'A']
    return sum(sum(ratings[rating].values()) for rating in accepted_ratigns)
        
        

def parse_input(input: str) -> list[list[str]]:
    return [section.splitlines() for section in input.split('\n\n')]


def parse_workflow(workflow: str) -> tuple[str, list[tuple[str, str, int, str]], str]:
    workflows_regex = r'([a-z]+)\{([^}]+)\}'
    id, steps = re.findall(workflows_regex, workflow)[0]
    
    steps = steps.split(',')
    last_step = steps.pop()
    parsed_steps = [(step[0], step[1], int(step.split(':')[0][2:]), step.split(':')[1]) for step in steps]
    
    return id, parsed_steps, last_step 


def parse_ratings(ratings: list[str]) -> list[dict[str, int]]:
    return [
        {part[0]: int(part[2:]) for part in rating} 
        for rating in (r[1:-1].split(',') for r in ratings)
    ]
    
    
def threshold_success(op: str, threshold: int, value: int) -> bool:
    match op:
        case '<':
            return value < threshold
        case '>':
            return value > threshold
        case _:
            raise ValueError(f"Operator not found: {op}")


def part_02(input: str) -> str:
    return "Part two answer"
