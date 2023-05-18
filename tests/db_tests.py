import os
from tempfile import TemporaryDirectory

from pytest import fixture, raises
from purecrypt import Crypt
from datetime import datetime

from gamedb import NoSuchGameError
from gamedb.json import JsonDatabase, JsonGameRepository

GID = "some-uid"
CREATOR = "some-creator"
PLAYER = "player0"
PLAYERS = tuple((PLAYER, "player1", "player2"))

@fixture
def json_database():
    dir = TemporaryDirectory()
    db_file = os.path.join(dir.name, "db.json")
    yield JsonDatabase(db_file)
    dir.cleanup()


@fixture
def game_repository(json_database):
    return JsonGameRepository(json_database)


def test_game_crud(game_repository):
    game = game_repository.create_game(CREATOR, PLAYERS)
    assert game.gid is not None
    assert game.creation_date is not None
    assert game.creator == CREATOR
    assert game.players == PLAYERS

    gid = game.gid
    game = game_repository.find_game(gid)
    assert game.gid == gid
    assert game.creation_date is not None
    assert game.creator == CREATOR
    assert game.players == PLAYERS

    games = tuple(game_repository.find_games_for_user(PLAYER))
    assert len(games) == 1
    assert games[0].gid == gid

    game.custom = True
    game = game_repository.replace_game(game)
    assert game.gid == gid
    assert game.creation_date is not None
    assert game.creator == CREATOR
    assert game.players == PLAYERS
    assert game.custom

    game_repository.delete_game(gid)

    with raises(NoSuchGameError):
        game_repository.find_game(gid)

def test_find_games_for_user(game_repository):
    game1 = game_repository.create_game(CREATOR, (PLAYER, "player3"))
    game2 = game_repository.create_game(CREATOR, (PLAYER, "player4"))
    game3 = game_repository.create_game(CREATOR, ("player5", "player6"))
    
    games = game_repository.find_games_for_user(PLAYER)
    assert len(games) == 2
    
def test_replace_game(game_repository):
    game = game_repository.create_game(CREATOR, PLAYERS)
    game.custom = False
    game = game_repository.replace_game(game)
    assert game.custom == False
    
    game.custom = True
    game = game_repository.replace_game(game)
    assert game.custom == True
    
    game2 = game_repository.find_game(game.gid)
    assert game2.custom == True
    
