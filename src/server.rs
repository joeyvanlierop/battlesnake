use std::env;

use log::info;
use rocket::{config::Environment, http::Status, Config};
use rocket_contrib::json::{Json, JsonValue};

use crate::{engine::GameState, logic};

#[get("/")]
fn handle_index() -> JsonValue {
    logic::get_info()
}

#[post("/start", format = "json", data = "<start_req>")]
fn handle_start(start_req: Json<GameState>) -> Status {
    logic::start(
        &start_req.game,
        &start_req.turn,
        &start_req.board,
        &start_req.you,
    );

    Status::Ok
}

#[post("/move", format = "json", data = "<move_req>")]
fn handle_move(move_req: Json<GameState>) -> JsonValue {
    let chosen = logic::get_move(
        &move_req.game,
        &move_req.turn,
        &move_req.board,
        &move_req.you,
    );

    return json!({ "move": chosen });
}

#[post("/end", format = "json", data = "<end_req>")]
fn handle_end(end_req: Json<GameState>) -> Status {
    logic::end(&end_req.game, &end_req.turn, &end_req.board, &end_req.you);

    Status::Ok
}

pub fn serve() {
    let address = "0.0.0.0";
    let env_port = env::var("PORT").ok();
    let env_port = env_port.as_ref().map(String::as_str).unwrap_or("8080");
    let port = env_port.parse::<u16>().unwrap();

    env_logger::init();

    let config = Config::build(Environment::Development)
        .address(address)
        .port(port)
        .finalize()
        .unwrap();

    info!(
        "Starting Battlesnake Server at http://{}:{}...",
        address, port
    );
    rocket::custom(config)
        .mount(
            "/",
            routes![handle_index, handle_start, handle_move, handle_end],
        )
        .launch();
}
