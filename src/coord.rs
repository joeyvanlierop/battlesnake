use serde::{Deserialize, Serialize};

#[derive(Copy, Clone, Deserialize, Serialize, PartialEq, Debug)]
pub struct Coord {
    pub x: u32,
    pub y: u32,
}
