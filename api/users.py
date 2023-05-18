from flask import request, g
from gamedb import DuplicateUserIdError, NoSuchUserError
from gameauth import encrypt_password, is_valid_password 
from .app import app, user_repository
from .errors import ForbiddenError, NotFoundError, PreconditionFailedError, PreconditionRequiredError, ValidationError

from .auth import authenticate
import time
from .props import *
import threading


###########################################################################
# This module handles API requests for the Users resource


from threading import Event, Lock

# Define a global Event object to signal when a user joins the waiting list
event = Event()
# Define a global Lock object to ensure safe access to the waiting_users list
waiting_users_lock = Lock()
waiting_users = []

# Create a new user and add to the repository
@app.route(USERS_PATH, methods=["POST"])
def create_user():
    if not request.is_json:
        raise ValidationError("request body must be JSON")

    input_data = request.get_json()
    uid = input_data.get(UID)
    password = input_data.get(PASSWORD)

    if not uid or not password:
        raise ValidationError("request must include UID and password")
    try:
        user = user_repository.create_user(uid, password)
    except DuplicateUserIdError:
        raise ValidationError(f"user {uid} already exists")

    output_data = user_to_dict(user)
    return output_data, 201, {"Location": output_data[HREF], "ETag": user.tag()}

# Add a user to the waiting list to join a game
@app.route(f"{USERS_PATH}/<uid>", methods=['POST'])
def join_game(uid: str):
    
    input_data = request.get_json()
    player_name = input_data.get(UID)
    player_password = input_data.get(PASSWORD)
    if uid is None:
        return 'Player name not specified', 400
    
    # Add the user to the waiting list
    add_waiting_user([player_name, player_password])
    start_time = time.time()
    
    # Check if there is a match within 120 seconds
    while time.time() - start_time < 120: # wait for up to 120 seconds
        with waiting_users_lock:
            if len(waiting_users) == 2 and waiting_users[1][0] == uid:
                event.clear()   
                return waiting_users, 200
            elif len(waiting_users) == 2 and waiting_users[0][0] == uid:
                event.clear()
                return [waiting_users[0]], 200
        event.wait(timeout=5)
    
    # If no match is found within 120 seconds, remove the user from the waiting list and return a 203 response
    remove_waiting_user(uid)
    return "", 203

# Add a user to the waiting list
def add_waiting_user(user: str):
    with waiting_users_lock:
        waiting_users.append(user)
        if len(waiting_users) == 2:
            event.set()

# Remove a user from the waiting list
def remove_waiting_user(player_name: str):
    with waiting_users_lock:
        if player_name in waiting_users:
            waiting_users.remove(player_name)
            if len(waiting_users) == 1:
                event.clear()

@app.route(f"{USERS_PATH}/<uid>")
def fetch_user(uid: str):
    """ Fetch an existing User object. """
    input_data = request.get_json()
    uid = input_data.get(UID)
    password = input_data.get(PASSWORD)
    try:    
        user = user_repository.find_user(uid)
    except NoSuchUserError:
        raise NotFoundError(f"user '{uid}' not found")
    if uid == user.uid and is_valid_password(password, user.password):
        return user_to_dict(user), 200, {"ETag": user.tag()}
    else:
        return "incorrect password", 201

@app.route(f"{USERS_PATH}/<uid>/password", methods=["PUT"])
@authenticate
def change_password(uid: str):
    """ Change a user's password """
    # Authenticated user must be the user whose password is to be changed
    if uid != g.uid:
        raise ForbiddenError()
    
    password = request.get_data(as_text=True)
    if not password:
        raise ValidationError("must provide new password")
    try:
        user_repository.change_password(uid, password)
    except NoSuchUserError:
        raise NotFoundError(f"user '{uid}' not found")
    
    return "", 204

@app.route(f"{USERS_PATH}/<uid>", methods=["DELETE"])
@authenticate
def delete_user(uid: str):
    """ Delete a user if it exists """
    # Authenticated user must be the user to be deleted
    if uid != g.uid:
        raise ForbiddenError()

    # The user repository doesn't complain when you try to delete
    # a user that doesn't exist, so no error handling needed here.
    user_repository.delete_user(uid)
    return "", 204
