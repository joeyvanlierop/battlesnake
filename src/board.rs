use std::collections::{HashMap, HashSet};

use serde::{Deserialize, Serialize};

use crate::{
    coord::Coord,
    snake::{Battlesnake, Direction},
};

const MAX_PLY: u8 = 50;

pub struct Ply {
    pub snake_index: usize,
    pub direction: Direction,
}

impl Ply {
    pub fn new(snake_index: usize, direction: Direction) -> Ply {
        Ply {
            snake_index,
            direction,
        }
    }
}

#[derive(Clone, PartialEq, Deserialize, Serialize, Debug)]
pub struct Board {
    pub height: i8,
    pub width: i8,
    pub food: Vec<Coord>,
    pub snakes: Vec<Battlesnake>,
}
impl Board {
    pub fn tick(&mut self, plies: &Vec<Ply>) {
        // Create a set to store a list of foods to remove after all plies have been completed
        let mut to_remove = HashSet::new();

        // Run all of the plies
        for ply in plies.iter() {
            let snake = &mut self.snakes[ply.snake_index];

            // Move the snake
            snake.do_move(&ply.direction);

            // Eat any food that the snake has landed on
            for (food_index, food) in self.food.iter().enumerate() {
                if snake.head == *food {
                    snake.eat();
                    to_remove.insert(food_index);
                }
            }
        }

        // Remove all consumed foods
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

    pub fn minimax(
        &self,
        ply: u8,
        plies: &mut Vec<Ply>,
        maximizing_index: usize,
        minimizing_index: usize,
    ) -> f64 {
        // An even ply indicates that it is the maximizing players turn
        // We should not evaluate or end a game while on an even ply
        if ply % 2 == 0 {
            // Branch out maximizing snake in all possible directions and store value
            // We do not evaluate the board at this moment
            for direction in Direction::iter() {
                plies.push(Ply::new(maximizing_index, direction));
                return self.minimax(ply + 1, plies, maximizing_index, minimizing_index);
            }
        }
        // An odd ply indicates that it is the minimizing players turn
        // We should evaluate the game while on an even ply
        else {
            // If we have reached the max depth we should evaluate the current position
            if ply >= MAX_PLY {
                return self.evaluate(minimizing_index);
            }

            // Otherwise, branch out minimizing snake in all possible directions
            for direction in Direction::iter() {
                plies.push(Ply::new(minimizing_index, direction));
                let mut board = self.clone();
                board.tick(&plies);
                return board.minimax(ply + 1, &mut vec![], maximizing_index, minimizing_index);
            }
        }

        return 0.;
    }

    pub fn evaluate(&self, snake_index: usize) -> f64 {
        // TODO: Implement
        return 0.;
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
            head: Coord::new(2, 0),
            body: vec![Coord::new(2, 0), Coord::new(1, 0), Coord::new(0, 0)],
        }],
    };
    let mut expected_board = board.clone();

    // Act
    board.tick(&vec![Ply::new(0, Direction::RIGHT)]);
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
        food: vec![Coord::new(3, 0), Coord::new(4, 0)],
        snakes: vec![Battlesnake {
            id: String::from("abc"),
            health: 50,
            length: 3,
            head: Coord::new(2, 0),
            body: vec![Coord::new(2, 0), Coord::new(1, 0), Coord::new(0, 0)],
        }],
    };
    let mut expected_board = board.clone();

    // Act
    board.tick(&vec![Ply::new(0, Direction::RIGHT)]);
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
                    head: Coord::new(2, 0),
                    body: vec![Coord::new(2, 0), Coord::new(1, 0), Coord::new(0, 0)],
                },
                Battlesnake {
                    id: String::from("def"),
                    health: 50,
                    length: 3,
                    head: Coord::new(2, 1),
                    body: vec![Coord::new(2, 1), Coord::new(2, 2), Coord::new(2, 3)],
                },
                Battlesnake {
                    id: String::from("ghi"),
                    health: 50,
                    length: 2,
                    head: Coord::new(3, 0),
                    body: vec![Coord::new(3, 0), Coord::new(4, 0)],
                },
            ],
        };

        // Act
        board.tick(&vec![Ply::new(0, test_case.0)]);

        // Assert
        assert_eq!(test_case.1, board.is_alive(0));
    }
}

#[test]
fn test_minimax() {
    // Arrange
    let board = Board {
        width: 5,
        height: 5,
        food: vec![],
        snakes: vec![
            Battlesnake {
                id: String::from("abc"),
                health: 50,
                length: 3,
                head: Coord::new(2, 0),
                body: vec![Coord::new(2, 0), Coord::new(1, 0), Coord::new(0, 0)],
            },
            Battlesnake {
                id: String::from("def"),
                health: 50,
                length: 3,
                head: Coord::new(2, 1),
                body: vec![Coord::new(2, 1), Coord::new(2, 2), Coord::new(2, 3)],
            },
        ],
    };

    let evaluation = board.minimax(0, &mut vec![], 0, 1);
    assert_eq!(evaluation, 1.)
}
