use std::collections::HashMap;

use crate::{board::Board, snake::Battlesnake};
use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize)]
pub struct GameState {
    pub game: Game,
    pub turn: u32,
    pub board: Board,
    pub you: Battlesnake,
}

#[derive(Deserialize, Serialize, Debug)]
pub struct Game {
    pub id: String,
    pub ruleset: HashMap<String, String>,
    pub timeout: u32,
}
