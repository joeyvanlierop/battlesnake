use serde::{Deserialize, Serialize};

use crate::{
    coord::Coord,
    snake::{Battlesnake, Direction},
};

#[derive(Clone, PartialEq, Deserialize, Serialize, Debug)]
pub struct Board {
    pub height: i8,
    pub width: i8,
    pub food: Vec<Coord>,
    pub snakes: Vec<Battlesnake>,
}
impl Board {
    pub fn tick(&mut self, snake_index: usize, direction: Direction) {
        let snake = &mut self.snakes[snake_index];

        // Move the snake
        snake.do_move(&direction);

        // Eat any food that the snake has landed on
        let to_remove = &mut vec![];
        for (food_index, food) in self.food.iter().enumerate() {
            if snake.head == *food {
                snake.eat();
                to_remove.push(food_index);
            }
        }
        for food_index in to_remove.iter() {
            self.food.remove(*food_index);
        }
    }

    pub fn is_alive(&self, snake_index: usize) -> bool {
        let snake = &self.snakes[snake_index];

        // Health less than or equal to 0
        if snake.health <= 0 {
            return false;
        }

        // Moved out of bounds
        if snake.head.x < 0
            || snake.head.y < 0
            || snake.head.x >= self.width
            || snake.head.y >= self.height
        {
            return false;
        }

        // Collided with themselves
        if snake.body.iter().filter(|b| **b == snake.head).count() > 1 {
            return false;
        }

        // Collision with another Battlesnake
        for other_snake in &self.snakes {
            if snake.id != other_snake.id {
                // Collided head-to-head
                if snake.head == other_snake.head {
                    if snake.length <= other_snake.length {
                        return false;
                    }
                }
                // Collided with body
                else if other_snake.body.contains(&snake.head) {
                    return false;
                }
            }
        }

        // Snake is not dead :)
        true
    }
}

#[test]
fn test_tick_normal() {
    // Arrange
    let mut board = Board {
        width: 5,
        height: 5,
        food: vec![],
        snakes: vec![Battlesnake {
            id: String::from("abc"),
            health: 50,
            length: 3,
            head: Coord { x: 2, y: 0 },
            body: vec![
                Coord { x: 2, y: 0 },
                Coord { x: 1, y: 0 },
                Coord { x: 0, y: 0 },
            ],
        }],
    };
    let mut expected_board = board.clone();

    // Act
    board.tick(0, Direction::RIGHT);
    expected_board.snakes[0].do_move(&Direction::RIGHT);

    // Assert
    assert_eq!(board, expected_board);
}

#[test]
fn test_tick_eat() {
    // Arrange
    let mut board = Board {
        width: 5,
        height: 5,
        food: vec![Coord { x: 3, y: 0 }, Coord { x: 4, y: 0 }],
        snakes: vec![Battlesnake {
            id: String::from("abc"),
            health: 50,
            length: 3,
            head: Coord { x: 2, y: 0 },
            body: vec![
                Coord { x: 2, y: 0 },
                Coord { x: 1, y: 0 },
                Coord { x: 0, y: 0 },
            ],
        }],
    };
    let mut expected_board = board.clone();

    // Act
    board.tick(0, Direction::RIGHT);
    expected_board.food.remove(0);
    expected_board.snakes[0].do_move(&Direction::RIGHT);
    expected_board.snakes[0].eat();

    // Assert
    assert_eq!(board, expected_board);
}

#[test]
fn test_die() {
    for test_case in [
        (Direction::UP, false),   // Collide with equal snake
        (Direction::RIGHT, true), // Collide with smaller snake
        (Direction::DOWN, false), // Move off of board
        (Direction::LEFT, false), // Collide with self
    ]
    .iter()
    {
        // Arrange
        let mut board = Board {
            width: 5,
            height: 5,
            food: vec![],
            snakes: vec![
                Battlesnake {
                    id: String::from("abc"),
                    health: 50,
                    length: 3,
                    head: Coord { x: 2, y: 0 },
                    body: vec![
                        Coord { x: 2, y: 0 },
                        Coord { x: 1, y: 0 },
                        Coord { x: 0, y: 0 },
                    ],
                },
                Battlesnake {
                    id: String::from("def"),
                    health: 50,
                    length: 3,
                    head: Coord { x: 2, y: 1 },
                    body: vec![
                        Coord { x: 2, y: 1 },
                        Coord { x: 2, y: 2 },
                        Coord { x: 2, y: 3 },
                    ],
                },
                Battlesnake {
                    id: String::from("ghi"),
                    health: 50,
                    length: 2,
                    head: Coord { x: 3, y: 0 },
                    body: vec![Coord { x: 3, y: 0 }, Coord { x: 4, y: 0 }],
                },
            ],
        };

        // Act
        board.tick(0, test_case.0);

        // Assert
        assert_eq!(test_case.1, board.is_alive(0));
    }
}
