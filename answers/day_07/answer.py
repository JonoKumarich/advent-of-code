from enum import Enum
from typing import TypeVar
from collections import defaultdict
from typing import DefaultDict, TypeVar
from collections import defaultdict
import bisect
from dataclasses import dataclass


T = TypeVar("T")
CARD_ORDERS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']


class HandType(Enum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


@dataclass
class Turn:
    hand: str
    bet: int
    
    def __lt__(self, other: "Turn") -> bool:
        for i in range(len(self.hand)):
            self_card, other_card = self.hand[i], other.hand[i]
            if self_card == other_card:
                continue
            
            self_rank = CARD_ORDERS.index(self_card)
            other_rank = CARD_ORDERS.index(other_card)
            return self_rank > other_rank
        
        raise ValueError("Two hands equal???")


def part_01(input: str) -> int:
    hands = parse_input(input)
    num_hand_types = len(HandType)
    values: list[list[Turn]] = [[] for _ in range(num_hand_types)]
    
    for turn in hands:
        hand_type = calculate_hand_type(turn.hand)
        bisect.insort(values[hand_type.value], turn)
    
    # Flatten
    scores = [item.bet for row in values for item in row]
    return sum([(i + 1) * score for i, score in enumerate(scores)])
    


def part_02(input: str) -> str:
    return "Part two answer"


def parse_input(input: str) -> list[Turn]:
    lines = [line.split() for line in input.splitlines()]
    return [Turn(hand, int(bet)) for (hand, bet) in lines]


def count_frequency(iterable: list[T]) -> DefaultDict[T, int]:
    frequencies: DefaultDict[T, int] = defaultdict(lambda: 0)
    
    for item in iterable:
        frequencies[item] += 1
    
    return frequencies


def calculate_hand_type(hand: str) -> HandType:
    frequencies = count_frequency(list(hand))
    
    match len(frequencies):
        case 1:
            return HandType.FIVE_OF_A_KIND
        case 2:
            four_cards = max(frequencies.values()) == 4
            return HandType.FOUR_OF_A_KIND if four_cards else HandType.FULL_HOUSE
        case 3:
            three_cards = max(frequencies.values()) == 3
            return HandType.THREE_OF_A_KIND if three_cards else HandType.TWO_PAIR
        case 4:
            return HandType.ONE_PAIR
        case 5:
            return HandType.HIGH_CARD
        case _:
            raise ValueError("Hand value can not be calculated")
    