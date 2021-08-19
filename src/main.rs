#![feature(proc_macro_hygiene, decl_macro)]

#[macro_use]
extern crate rocket;
#[macro_use]
extern crate rocket_contrib;

mod board;
mod coord;
mod game_state;
mod logic;
mod server;
mod snake;

fn main() {
    server::serve()
}
