
from movement.directions import Direction, remove_direction
from typing import Dict, List


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[Direction]) -> List[Direction]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of directions. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of ris it emaining possible_moves, with the 'neck' direction removed
    """
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    # Neck is left of head
    if my_neck["x"] < my_head["x"]:
        possible_moves = remove_direction(Direction.LEFT, possible_moves)
    # Neck is right of head
    elif my_neck["x"] > my_head["x"]:
        possible_moves = remove_direction(Direction.RIGHT, possible_moves)
    # Neck is below head
    elif my_neck["y"] < my_head["y"]:
        possible_moves = remove_direction(Direction.DOWN, possible_moves)
    # Neck is above head
    elif my_neck["y"] > my_head["y"]:
        possible_moves = remove_direction(Direction.UP, possible_moves)

    return possible_moves


def avoid_body(my_head: Dict[str, int], body: List[dict], possible_moves: List[Direction]) -> List[Direction]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of directions. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves which don't run into my snakes body
    """
    up = {"x": my_head["x"], "y": my_head["y"] + 1}
    down = {"x": my_head["x"], "y": my_head["y"] - 1}
    left = {"x": my_head["x"] - 1, "y": my_head["y"]}
    right = {"x": my_head["x"] + 1, "y": my_head["y"]}
    # Body is left of head
    if left in body:
        possible_moves = remove_direction(Direction.LEFT, possible_moves)
    # Body is right of head
    if right in body:
        possible_moves = remove_direction(Direction.RIGHT, possible_moves)
    # Body is below head
    if down in body:
        possible_moves = remove_direction(Direction.DOWN, possible_moves)
    # Body is above head
    if up in body:
        possible_moves = remove_direction(Direction.UP, possible_moves)

    return possible_moves


def avoid_board_edge(my_head: Dict[str, int], board_height: int, board_width: int, possible_moves: List[Direction]) -> List[Direction]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    possible_moves: List of directions. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'board edge' direction removed
    """
    # Head is on left edge of the board
    if my_head["x"] == 0:
        possible_moves = remove_direction(Direction.LEFT, possible_moves)
    # Head is on right edge of the board
    elif my_head["x"] == board_width - 1:
        possible_moves = remove_direction(Direction.RIGHT, possible_moves)
    # Head is on bottom edge of the board
    if my_head["y"] == 0:
        possible_moves = remove_direction(Direction.DOWN, possible_moves)
    # Head is on top edge of the board
    elif my_head["y"] == board_height - 1:
        possible_moves = remove_direction(Direction.UP, possible_moves)

    return possible_moves
