from backend import app

from backend.controllers import pokemon_controller
from backend.controllers import battle_controller

if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=True)