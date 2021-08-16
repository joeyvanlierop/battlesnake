import unittest
import copy
from simulation import Board, Move, next_state, is_alive


class TestNextMove(unittest.TestCase):
    def setUp(self):
        self.board: Board = {
            "height": 5,
            "width": 5,
            "food": [],
            "snakes": [
                {
                    "id": "abc",
                    "health": 50,
                    "body": [
                        {"x": 1, "y": 1},
                        {"x": 2, "y": 1},
                        {"x": 3, "y": 1}
                    ],
                    "head": {"x": 1, "y": 1},
                    "length": 3,
                }
            ]
        }

    def test_move(self):
        for direction, head in [("up", {"x": 1, "y": 2}), ("right", {"x": 2, "y": 1}), ("down", {"x": 1, "y": 0}), ("left", {"x": 0, "y": 1})]:
            with self.subTest(direction=direction):
                # Arrange
                move: Move = {
                    "id": "abc",
                    "direction": direction
                }
                test_board = copy.deepcopy(self.board)
                test_board["snakes"][0]["health"] -= 1
                test_board["snakes"][0]["head"] = head
                test_board["snakes"][0]["body"].pop()
                test_board["snakes"][0]["body"].insert(0, head)

                # Act
                state = next_state(self.board, move)
                # Assert
                self.assertDictEqual(state, test_board)

    def test_eat(self):
        # Arrange
        max_health = 42
        move: Move = {
            "id": "abc",
            "direction": "up"
        }
        head = {
            "x": 1,
            "y": 2,
        }
        self.board["food"].append(head)
        test_board = copy.deepcopy(self.board)
        test_board["food"].remove(head)
        test_board["snakes"][0]["health"] = max_health
        test_board["snakes"][0]["length"] += 1
        test_board["snakes"][0]["head"] = head
        test_board["snakes"][0]["body"].pop()
        test_board["snakes"][0]["body"].append({"x": 2, "y": 1})
        test_board["snakes"][0]["body"].insert(0, head)

        # Act
        state = next_state(self.board, move, max_health)

        # Assert
        self.assertDictEqual(state, test_board)


class TestIsAlive(unittest.TestCase):
    def setUp(self):
        self.board: Board = {
            "height": 5,
            "width": 5,
            "food": [
                {"x": 5, "y": 6},
                {"x": 9, "y": 0},
                {"x": 2, "y": 6}
            ],
            "snakes": [
                {
                    "id": "abc",
                    "health": 50,
                    "body": [
                        {"x": 1, "y": 1},
                        {"x": 2, "y": 1},
                        {"x": 3, "y": 1}
                    ],
                    "head": {"x": 1, "y": 1},
                    "length": 3,
                }
            ]
        }

    def test_alive(self):
        # Act
        alive = is_alive(self.board, "abc")

        # Assert
        self.assertTrue(alive)

    def test_out_of_health(self):
        for health in [0, -1]:
            with self.subTest(health=health):
                # Arrange
                test_board = copy.deepcopy(self.board)
                test_board["snakes"][0]["health"] = health

                # Act
                alive = is_alive(test_board, test_board["snakes"][0]["id"])

                # Assert
                self.assertFalse(alive)

    def test_out_of_bounds(self):
        for axis, coordinate in [("y", self.board["height"]), ("x", self.board["width"]), ("y", -1), ("x", -1)]:
            with self.subTest(axis=axis, coordinate=coordinate):
                # Arrange
                test_board = copy.deepcopy(self.board)
                test_board["snakes"][0]["head"][axis] = coordinate

                # Act
                alive = is_alive(test_board, test_board["snakes"][0]["id"])

                # Assert
                self.assertFalse(alive)

    def test_collided_with_self(self):
        # Arrange
        test_board = copy.deepcopy(self.board)
        test_board["snakes"][0]["head"] = test_board["snakes"][0]["body"][1]
        test_board["snakes"][0]["body"].pop()
        test_board["snakes"][0]["body"].insert(
            0, test_board["snakes"][0]["head"])

        # Act
        alive = is_alive(test_board, test_board["snakes"][0]["id"])

        # Assert
        self.assertFalse(alive)

    def test_collided_with_other(self):
        # Arrange
        self.board["snakes"].append(
            {
                "id": "def",
                "health": 50,
                "body": [
                    {"x": 1, "y": 0},
                    {"x": 1, "y": 1},
                    {"x": 1, "y": 2}
                ],
                "head": {"x": 1, "y": 0},
                "length": 3,
            }
        )

        # Act
        alive = is_alive(self.board, "abc")

        # Assert
        self.assertFalse(alive)

    def test_collided_with_other_head(self):
        for other_length, should_live in [(2, True), (3, False), (4, False)]:
            with self.subTest(other_length=other_length, should_live=should_live):
                # Arrange
                test_board = copy.deepcopy(self.board)
                test_board["snakes"].append(
                    {
                        "id": "def",
                        "head": {"x": 1, "y": 1},
                        "length": other_length,
                    }
                )

                # Act
                alive = is_alive(test_board, "abc")

                # Assert
                self.assertEqual(alive, should_live)


if __name__ == "__main__":
    unittest.main()
