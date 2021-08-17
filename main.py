import logging
from server import run

if __name__ == "__main__":
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    run()
