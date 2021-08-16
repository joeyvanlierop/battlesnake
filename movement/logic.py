from movement.targeting import find_closest_food, move_towards_food
from movement.directions import Direction
from movement.avoidance import avoid_board_edge, avoid_body, avoid_my_neck
import random


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

    possible_moves = [Direction.UP, Direction.LEFT,
                      Direction.DOWN, Direction.RIGHT]

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
    possible_moves = move_towards_food(my_head, closest_food, possible_moves)

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    move = random.choice(possible_moves)

    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
