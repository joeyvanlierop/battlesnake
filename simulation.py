import copy
from typing import List, TypedDict


class Coordinate(TypedDict):
    x: int
    y: int


class Snake(TypedDict):
    id: str
    name: str
    health: int
    length: int
    head: Coordinate
    body: List[Coordinate]


class Board(TypedDict):
    height: int
    width: int
    food: List[Coordinate]
    snakes: List[Snake]


class Move(TypedDict):
    id: str
    direction: str


def is_alive(board: Board, id: str) -> bool:
    """ Determines if the Battlesnake with the given id shuold be considered alive

    The Battlesnake is determined to be alive according to the Battlesnake game engine rules:
    https://docs.battlesnake.com/references/rules#3-moves-are-resolved-by-the-game-engine
    """

    # Find snake
    snake = next(s for s in board["snakes"] if s["id"] == id)

    # Health less than or equal to 0
    if snake["health"] <= 0:
        return False

    # Moved out of bounds
    if snake["head"]["x"] < 0 or snake["head"]["y"] < 0 or snake["head"]["x"] >= board["width"] or snake["head"]["y"] >= board["height"]:
        return False

    # Collided with themselves
    if snake["body"].count(snake["head"]) > 1:
        return False

    # Collided with another Battlesnake
    for other_snake in board["snakes"]:
        if snake["id"] != other_snake["id"]:
            # Collided head-to-head
            if snake["head"] == other_snake["head"]:
                if snake["length"] <= other_snake["length"]:
                    return False
            # Collided with the body
            elif snake["head"] in other_snake["body"]:
                return False

    # Snake is not dead :)
    return True


def next_state(board: Board, move: Move, max_health=100) -> Board:
    """ Determines the next board state according

    The next state is determined according to the Battlesnake game engine rules:
    https://docs.battlesnake.com/references/rules#3-moves-are-resolved-by-the-game-engine
    """

    # Create our new instance of the board
    new_board = copy.deepcopy(board)

    # Make the given move
    for snake in new_board["snakes"]:
        if snake["id"] == move["id"]:
            # A new body part is added to the board in the direction they moved.
            new_x = snake["head"]["x"]
            new_y = snake["head"]["y"]
            if move["direction"] == "up":
                new_y += 1
            elif move["direction"] == "right":
                new_x += 1
            elif move["direction"] == "down":
                new_y -= 1
            elif move["direction"] == "left":
                new_x -= 1
            new_head = {
                "x": new_x,
                "y": new_y,
            }
            snake["head"] = new_head
            snake["body"].insert(0, new_head)

            # Last body part (their tail) is removed from the board.
            snake["body"].pop()

            # Health is reduced by 1.
            snake["health"] -= 1

            # Any Battlesnake that has found food will consume it
            if snake["head"] in new_board["food"]:
                # Health reset set maximum
                snake["health"] = max_health

                # Additional body part placed on top of current tail
                snake["body"].append(snake["body"][-1])
                snake["length"] += 1

                # The food is removed from the board
                new_board["food"].remove(snake["head"])

    return new_board
