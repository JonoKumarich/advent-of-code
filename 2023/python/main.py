import argparse
import importlib
from pathlib import Path

def run_day(day: int, part: int, test: bool) -> None:
    day_module = importlib.import_module(f"answers.day_{day:02d}.answer")

    run_type = f'test_{part:02d}' if test else 'input'
    
    input_path = Path(__file__).parent / f"answers/day_{day:02d}/{run_type}.txt"
    with open(input_path) as f:
        input = f.read()
    
    print(f"Running {run_type} Case {day}, Part {part}")
    output = getattr(day_module, f"part_{part:02d}")(input)
    
    print(f"Output: \n{output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Advent of Code solutions.")
    parser.add_argument("--day", type=int, required=True, help="Day of the challenge")
    parser.add_argument("--part", type=int, choices=[1, 2], required=True, help="Part of the challenge")
    parser.add_argument("--test", action="store_true", help="Run the test case")

    args = parser.parse_args()
    run_day(args.day, args.part, args.test)
