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

    # Neck is left of head
    if my_neck["x"] < my_head["x"]:
        possible_moves = remove_direction("left", possible_moves)
    # Neck is right of head
    elif my_neck["x"] > my_head["x"]:
        possible_moves = remove_direction("right", possible_moves)
    # Neck is below head
    elif my_neck["y"] < my_head["y"]:
        possible_moves = remove_direction("down", possible_moves)
    # Neck is above head
    elif my_neck["y"] > my_head["y"]:
        possible_moves = remove_direction("up", possible_moves)

    return possible_moves


def avoid_body(my_head: Dict[str, int], body: List[dict], possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves which don't run into my snakes body
    """
    up = {"x": my_head["x"], "y": my_head["y"] + 1}
    down = {"x": my_head["x"], "y": my_head["y"] - 1}
    left = {"x": my_head["x"] - 1, "y": my_head["y"]}
    right = {"x": my_head["x"] + 1, "y": my_head["y"]}
    # Body is left of head
    if left in body:
        possible_moves = remove_direction("left", possible_moves)
    # Body is right of head
    if right in body:
        possible_moves = remove_direction("right", possible_moves)
    # Body is below head
    if down in body:
        possible_moves = remove_direction("down", possible_moves)
    # Body is above head
    if up in body:
        possible_moves = remove_direction("up", possible_moves)

    return possible_moves


def avoid_board_edge(my_head: Dict[str, int], board_height: int, board_width: int, possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'board edge' direction removed
    """
    # Head is on left edge of the board
    if my_head["x"] == 0:
        possible_moves = remove_direction("left", possible_moves)
    # Head is on right edge of the board
    elif my_head["x"] == board_width - 1:
        possible_moves = remove_direction("right", possible_moves)
    # Head is on bottom edge of the board
    if my_head["y"] == 0:
        possible_moves = remove_direction("down", possible_moves)
    # Head is on top edge of the board
    elif my_head["y"] == board_height - 1:
        possible_moves = remove_direction("up", possible_moves)

    return possible_moves


def find_closest_food(my_head: Dict[str, int], foods: List[Dict[str, int]]) -> Dict[str, int]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    foods: List of dictionaries of x/y coordinates for every food location on the board.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The closest
    """
    closest_distance = None
    closest_food = None
    for food in foods:
        x_offset = my_head["x"] - food["x"]
        y_offset = my_head["y"] - food["y"]
        distance = x_offset ** 2 + y_offset ** 2
        if closest_distance is None or distance < closest_distance:
            closest_distance = distance
            closest_food = food

    print(closest_food)
    return closest_food


def move_towards_food(my_head: Dict[str, int], food: Dict[str, int], possible_moves: List[str]) -> str:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    food: Dictionary of x/y coordinates of the food location.
            e.g. {"x": 0, "y": 0}
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The move which moves towards the closest food location
    """
    if food is None:
        return random.choice(possible_moves)

    towards_moves = []

    # Head is left of the food
    if my_head["x"] > food["x"]:
        if "left" in possible_moves:
            towards_moves.append("left")
    # Head is right of the food
    elif my_head["x"] < food["x"]:
        if "right" in possible_moves:
            towards_moves.append("right")
    # Head is above the food
    if my_head["y"] > food["y"]:
        if "down" in possible_moves:
            towards_moves.append("down")
    # Head is below the food
    elif my_head["y"] < food["y"]:
        if "up" in possible_moves:
            towards_moves.append("up")

    return random.choice(towards_moves)


def remove_direction(direction: str, possible_moves: List[str]) -> List[str]:
    if direction in possible_moves:
        possible_moves.remove(direction)
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

    # Prevent snake from hitting any snakes
    snakes = data["board"]["snakes"]
    for snake in snakes:
        body = snake["body"]
        possible_moves = avoid_body(my_head, body, possible_moves)

    # Prevent snake from moving off the edge of the board
    board_height = data["board"]["height"]
    board_width = data["board"]["width"]
    possible_moves = avoid_board_edge(
        my_head, board_height, board_width, possible_moves)

    # Move towards the closest food
    food = data["board"]["food"]
    closest_food = find_closest_food(my_head, food)
    move = move_towards_food(my_head, closest_food, possible_moves)

    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
