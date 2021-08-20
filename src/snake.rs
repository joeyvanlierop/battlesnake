use serde::{Deserialize, Serialize};

use crate::coord::Coord;

const MAX_HEALTH: u8 = 100;

#[derive(Copy, Clone, Deserialize, Serialize, PartialEq, Debug)]
pub enum Direction {
    UP,
    RIGHT,
    DOWN,
    LEFT,
}

impl Direction {
    pub fn iter() -> impl Iterator<Item = Direction> {
        [
            Direction::UP,
            Direction::RIGHT,
            Direction::DOWN,
            Direction::LEFT,
        ]
        .iter()
        .copied()
    }
}

#[derive(Clone, Deserialize, Serialize, PartialEq, Debug)]
pub struct Battlesnake {
    pub id: String,
    pub health: u8,
    pub length: u8,
    pub body: Vec<Coord>,
    pub head: Coord,
}

impl Battlesnake {
    pub fn do_move(&mut self, direction: &Direction) {
        // Get the coordinates of the new head position
        let mut new_x = self.head.x;
        let mut new_y = self.head.y;
        match direction {
            Direction::UP => new_y += 1,
            Direction::RIGHT => new_x += 1,
            Direction::DOWN => new_y -= 1,
            Direction::LEFT => new_x -= 1,
        }

        // Create and assign the new head
        let new_head = Coord::new(new_x, new_y);
        self.head = new_head;
        self.body.insert(0, new_head);

        // Remove the current tail
        self.body.pop();

        // Reduce health by 1
        self.health -= 1;
    }

    pub fn eat(&mut self) {
        // Reset health to maximum
        self.health = MAX_HEALTH;

        // Extend body
        let new_tail = self.body.last().unwrap().clone();
        self.body.push(new_tail);
        self.length += 1
    }
}
