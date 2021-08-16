from movement.directions import Direction
import unittest

from movement.avoidance import avoid_my_neck, avoid_body


class AvoidNeckTest(unittest.TestCase):
    def test_avoid_neck_all(self):
        """
        The possible move set should be all moves.

        In the starter position, a Battlesnake body is 'stacked' in a
        single place, and thus all directions are valid.
        """
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 5, "y": 5}, {"x": 5, "y": 5}]
        possible_moves = [Direction.UP, Direction.DOWN,
                          Direction.LEFT, Direction.RIGHT]

        # Act
        result_moves = avoid_my_neck(test_head, test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), 4)
        self.assertEqual(possible_moves, result_moves)

    def test_avoid_neck_left(self):
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 4, "y": 5}, {"x": 3, "y": 5}]
        possible_moves = [Direction.UP, Direction.DOWN,
                          Direction.LEFT, Direction.RIGHT]
        expected = [Direction.UP, Direction.DOWN, Direction.RIGHT]

        # Act
        result_moves = avoid_my_neck(test_head, test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), len(expected))
        self.assertEqual(expected, result_moves)

    def test_avoid_neck_right(self):
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 6, "y": 5}, {"x": 7, "y": 5}]
        possible_moves = [Direction.UP, Direction.DOWN,
                          Direction.LEFT, Direction.RIGHT]
        expected = [Direction.UP, Direction.DOWN, Direction.LEFT]

        # Act
        result_moves = avoid_my_neck(test_head, test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), len(expected))
        self.assertEqual(expected, result_moves)

    def test_avoid_neck_up(self):
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 5, "y": 6}, {"x": 5, "y": 7}]
        possible_moves = [Direction.UP, Direction.DOWN,
                          Direction.LEFT, Direction.RIGHT]
        expected = [Direction.DOWN, Direction.LEFT, Direction.RIGHT]

        # Act
        result_moves = avoid_my_neck(test_head, test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), len(expected))
        self.assertEqual(expected, result_moves)

    def test_avoid_neck_down(self):
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 5, "y": 4}, {"x": 5, "y": 3}]
        possible_moves = [Direction.UP, Direction.DOWN,
                          Direction.LEFT, Direction.RIGHT]
        expected = [Direction.UP, Direction.LEFT, Direction.RIGHT]

        # Act
        result_moves = avoid_my_neck(test_head, test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), len(expected))
        self.assertEqual(expected, result_moves)


class AvoidBodyTest(unittest.TestCase):
    def test_avoid_self_all(self):
        """
        The possible move set should be all moves.

        In the starter position, a Battlesnake body is 'stacked' in a
        single place, and thus all directions are valid.
        """
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 5, "y": 5}, {"x": 5, "y": 5}]
        possible_moves = [Direction.UP, Direction.DOWN,
                          Direction.LEFT, Direction.RIGHT]

        # Act
        result_moves = avoid_body(test_head, test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), 4)
        self.assertEqual(possible_moves, result_moves)

    def test_avoid_body_left(self):
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 4, "y": 5}, {"x": 3, "y": 5}]
        possible_moves = [Direction.UP, Direction.DOWN,
                          Direction.LEFT, Direction.RIGHT]
        expected = [Direction.UP, Direction.DOWN, Direction.RIGHT]

        # Act
        result_moves = avoid_body(test_head, test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), len(expected))
        self.assertEqual(expected, result_moves)

    def test_avoid_body_right(self):
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 6, "y": 5}, {"x": 7, "y": 5}]
        possible_moves = [Direction.UP, Direction.DOWN,
                          Direction.LEFT, Direction.RIGHT]
        expected = [Direction.UP, Direction.DOWN, Direction.LEFT]

        # Act
        result_moves = avoid_body(test_head, test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), len(expected))
        self.assertEqual(expected, result_moves)

    def test_avoid_body_up(self):
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 5, "y": 6}, {"x": 5, "y": 7}]
        possible_moves = [Direction.UP, Direction.DOWN,
                          Direction.LEFT, Direction.RIGHT]
        expected = [Direction.DOWN, Direction.LEFT, Direction.RIGHT]

        # Act
        result_moves = avoid_body(test_head, test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), len(expected))
        self.assertEqual(expected, result_moves)

    def test_avoid_body_down(self):
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 5, "y": 4}, {"x": 5, "y": 3}]
        possible_moves = [Direction.UP, Direction.DOWN,
                          Direction.LEFT, Direction.RIGHT]
        expected = [Direction.UP, Direction.LEFT, Direction.RIGHT]

        # Act
        result_moves = avoid_body(test_head, test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), len(expected))
        self.assertEqual(expected, result_moves)

    def test_avoid_body_multiple(self):
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 5, "y": 4},
                     {"x": 4, "y": 4}, {"x": 4, "y": 5}]
        possible_moves = [Direction.UP, Direction.DOWN,
                          Direction.LEFT, Direction.RIGHT]
        expected = [Direction.UP, Direction.RIGHT]

        # Act
        result_moves = avoid_body(test_head, test_body, possible_moves)

        # Assert
        self.assertEqual(len(result_moves), len(expected))
        self.assertEqual(expected, result_moves)


if __name__ == "__main__":
    unittest.main()
