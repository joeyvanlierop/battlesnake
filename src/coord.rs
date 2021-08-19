use serde::{Deserialize, Serialize};

#[derive(Copy, Clone, Deserialize, Serialize, PartialEq, Debug)]
pub struct Coord {
    pub x: i8,
    pub y: i8,
}
