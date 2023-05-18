
from flask import Flask

from pymongo import MongoClient
from gameauth import TokenGenerator
from gamedb.mongo import MongoGameRepository, MongoUserRepository
from gamedb.json import JsonDatabase, JsonUserRepository, JsonGameRepository

import api.config as config

app = Flask(__name__)

DB_FILE = "db.json"

db = JsonDatabase(DB_FILE)
user_repository = JsonUserRepository(db)
game_repository = JsonGameRepository(db)


token_generator = TokenGenerator(issuer_uri=config.TOKEN_ISSUER_URI,
                                 private_key_filename=config.PRIVATE_KEY_FILE,
                                 private_key_passphrase=config.PRIVATE_KEY_PASSPHRASE)
