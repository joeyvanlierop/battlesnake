import math
from simulation import Board


def minimax(board: Board, remaining_depth: int, is_maximizing: bool, my_id: str):
    if remaining_depth == 0:
        return evaluate(board, my_id)


def evaluate(board: Board, my_id: str) -> float:
    return math.inf
