from typing import Dict, List
from movement.directions import Direction
import random


def find_closest_food(my_head: Dict[str, int], foods: List[Dict[str, int]]) -> Dict[str, int]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    foods: List of dictionaries of x/y coordinates for every food location on the board.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of directions. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The closest food location
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

    return closest_food


def move_towards_food(my_head: Dict[str, int], food: Dict[str, int], possible_moves: List[Direction]) -> List[Direction]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    food: Dictionary of x/y coordinates of the food location.
            e.g. {"x": 0, "y": 0}
    possible_moves: List of directions. Moves to pick from.
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

    if len(towards_moves) == 0:
        return possible_moves
    return towards_moves
