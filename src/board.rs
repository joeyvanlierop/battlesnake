use serde::{Deserialize, Serialize};

use crate::{
    coord::Coord,
    snake::{Battlesnake, Direction},
};

#[derive(Deserialize, Serialize)]
pub struct Board {
    pub height: u32,
    pub width: u32,
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
        if snake.head.x <= 0
            || snake.head.y <= 0
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
    let board = &mut Board {
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

    // Act
    board.tick(0, Direction::RIGHT);

    // Assert
    assert_eq!(board.snakes[0].body.len(), 3);
    assert_eq!(*board.snakes[0].body.last().unwrap(), Coord { x: 1, y: 0 });
    assert_eq!(board.snakes[0].head.x, 3);
    assert_eq!(board.snakes[0].health, 49);
}

#[test]
fn test_tick_eat() {
    // Arrange
    let board = &mut Board {
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

    // Act
    board.tick(0, Direction::RIGHT);

    // Assert
    assert_eq!(board.snakes[0].body.len(), 4);
    assert_eq!(*board.snakes[0].body.last().unwrap(), Coord { x: 1, y: 0 });
    assert_eq!(board.snakes[0].head.x, 3);
    assert_eq!(board.snakes[0].health, 100);
    assert_eq!(board.food.len(), 1);
    assert_eq!(board.food[0], Coord { x: 4, y: 0 });
}
