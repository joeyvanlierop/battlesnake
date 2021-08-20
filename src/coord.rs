use serde::{Deserialize, Serialize};

#[derive(Copy, Clone, Deserialize, Serialize, PartialEq, Debug)]
pub struct Coord {
    pub x: i8,
    pub y: i8,
}

impl Coord {
    pub fn new(x: i8, y: i8) -> Coord {
        Coord { x, y }
    }
}
