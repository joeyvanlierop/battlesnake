from enum import Enum
from typing import List


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


def remove_direction(direction: str, possible_moves: List[Direction]) -> List[Direction]:
    if direction in possible_moves:
        possible_moves.remove(direction)
    return possible_moves
