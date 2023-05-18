from flask import request, g

from gamedb import NoSuchUserError

from .app import app, game_repository, user_repository, token_generator
from .users import waiting_users
from .errors import ValidationError
from .auth import authenticate
from .props import *
from threading import Lock


game_info = Lock()  # A lock to ensure thread safety for game creation and deletion
@authenticate  # Ensure that user is authenticated to access these routes
@app.route(GAMES_PATH, methods=["POST"])
def create_game():
    if not request.is_json:
        raise ValidationError("request body must be JSON")
    requester = request.get_json()
    players = requester["players"]
    
    if len(players) == 1:  # If only one player is specified
        try:
            with game_info:  # Acquire lock to ensure thread safety
                games = game_repository.find_games_for_user(players[0])
                if games:
                    gamer = games[0]
                    token = token_generator.generate(players[0], gamer.gid, gamer.players)
                    data = game_to_dict(gamer, token)
                    return data, 201, {"Location": data[HREF]}
        except NoSuchUserError:
            raise ValidationError("must specify two or more players")
    else:
        player = None
        try:
            with game_info:  # Acquire lock to ensure thread safety
                for player in players:
                    user_repository.find_user(player)
                game = game_repository.create_game(players[0], players)
                waiting_users.clear()  # Clear the list of waiting users since a game has started
                token = token_generator.generate(players[1], game.gid, game.players)
                data = game_to_dict(game, token)
                return data, 201, {"Location": data[HREF]}
        except NoSuchUserError: 
            raise ValidationError(f"player '{player}' not found")


@app.route(f"{GAMES_PATH}/<gid>", methods=["DELETE"])
@authenticate
def delete_game(gid : str):
    try:
        with game_info:  # Acquire lock to ensure thread safety
            game = game_repository.find_game(gid)
            game_repository.delete_game(game.gid)
            return "", 204
    except NoSuchUserError:
            raise ValidationError("must specify two or more players")  # If no game with given ID is found, raise a validation error.
