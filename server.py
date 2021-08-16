import os

from flask import Flask, request

from movement import logic

app = Flask(__name__)


@app.get("/")
def handle_info():
    """
    This function is called when you register your Battlesnake on play.battlesnake.com
    See https://docs.battlesnake.com/guides/getting-started#step-4-register-your-battlesnake

    It controls your Battlesnake appearance and author permissions.
    For customization options, see https://docs.battlesnake.com/references/personalization

    TIP: If you open your Battlesnake URL in browser you should see this data.
    """
    print("INFO")
    return {
        "apiversion": "1",
        "author": "joeyvanlierop",
        "color": "#ff6392",
        "head": "sand-worm",
        "tail": "round-bum",
    }


@app.post("/start")
def handle_start():
    """
    This function is called everytime your snake is entered into a game.
    request.json contains information about the game that's about to be played.
    """
    data = request.get_json()

    print(f"{data['game']['id']} START")
    return "ok"


@app.post("/move")
def handle_move():
    """
    This function is called on every turn of a game. It's how your snake decides where to move.
    Valid moves are "up", "down", "left", or "right".
    """
    data = request.get_json()

    move = logic.choose_move(data)

    return {"move": move}


@app.post("/end")
def end():
    """
    This function is called when a game your snake was in ends.
    It's purely for informational purposes, you don't have to make any decisions here.
    """
    data = request.get_json()

    print(f"{data['game']['id']} END")
    return "ok"


@app.get("/metadata")
def metadata():
    """
    This function is used to verify the metadata of the battlesnake.
    It's purely for informational purposes, and will only be valuable when running on heroku.
    """
    print("VERSION")
    return {
        "created_at": os.environ.get("HEROKU_RELEASE_CREATED_AT"),
        "release_version": os.environ.get("HEROKU_RELEASE_VERSION"),
        "slug_commit": os.environ.get("HEROKU_SLUG_COMMIT"),
        "slug_description": os.environ.get("HEROKU_SLUG_DESCRIPTION"),
    }


def run():

    print("Starting Battlesnake Server...")
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=True)
