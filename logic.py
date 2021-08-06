import random
from typing import List, Dict


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:    # Neck is left of head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # Neck is right of head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # Neck is below head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # Neck is above head
        possible_moves.remove("up")

    return possible_moves


def avoid_board_edge(my_head: Dict[str, int], board_height: int, board_width: int, possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'board edge' direction removed
    """
    if my_head["x"] == 0:                   # Head is on left edge of the board
        possible_moves.remove("left")
    elif my_head["x"] == board_width - 1:   # Head is on right edge of the board
        possible_moves.remove("right")
    if my_head["y"] == 0:                   # Head is on bottom edge of the board
        possible_moves.remove("down")
    elif my_head["y"] == board_height - 1:  # Head is on top edge of the board
        possible_moves.remove("up")

    return possible_moves


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    my_body = data["you"]["body"]

    # Log data
    print(
        f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    print(f"All board data this turn: {data}")
    print(f"My Battlesnakes head this turn is: {my_head}")
    print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # Prevent snake from moving back in on it's own neck
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)

    # Prevent snake from moving off the edge of the board
    board_height = data["board"]["height"]
    board_width = data["board"]["width"]
    possible_moves = avoid_board_edge(
        my_head, board_height, board_width, possible_moves)

    # TODO Using information from 'data', don't let your Battlesnake pick a move that would hit its own body

    # TODO: Using information from 'data', don't let your Battlesnake pick a move that would collide with another Battlesnake

    # TODO: Using information from 'data', make your Battlesnake move towards a piece of food on the board

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    move = random.choice(possible_moves)
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
