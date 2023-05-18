Card Game War
================
War is a classic card game that is played by two players. The game is typically played with a standard deck of 52 playing cards, although specialized decks with different numbers of cards can also be used.

To play the game, the deck of cards is shuffled and divided equally among the players. Each player takes the top card from their deck and places it face up on the table. The player with the higher card wins the round and takes both cards, adding them to the bottom of their own deck. If both players have cards of equal value, a "war" is declared, where each player draws three additional cards and places them face down on the table. They then draw another card and place it face up on top of the pile, and the player with the higher card wins all of the cards in the pile. If there is another tie, the process is repeated until one player wins.

The game continues until one player has won all of the cards in the deck

* [Set Up the Virtual Environment](#set-up-the-virtual-environment)
* [Create a Key Pair](#create-a-key-pair)
* [Reactivating the Virtual Environment](#reactivating-the-virtual-environment)
* [Running the Server](#running-the-server)
* [Running the Client UI](#running-the-client-ui)
* [Running Everything](#running-everything)

Set Up the Virtual Environment
------------------------------

Clone this repository onto your local system and then follow the directions
below that apply to your system.

### Mac OS X

Create a Python virtual environment in the `.venv` subdirectory of the base
directory.
```bash
python3 -m venv .venv
```
Activate the virtual environment. This should change the prompt in some manner 
so that it displays the string `.venv` to remind you that the virtual 
environment has been activated.
```bash
source .venv/bin/activate
```
Install the dependencies needed to run the tests for the model.
```bash
python3 -m pip install -r requirements.txt
```
After successfully setting up the virtual environment you can 
now [Create a Key Pair](#create-a-key-pair) needed to run the API and the 
example server.

### Windows Command Prompt

```
py -m venv .venv
```

Activate the virtual environment. This should change the prompt in some manner 
so that it displays the string `.venv` to remind you that the virtual 
environment has been activated.
```
.venv\Scripts\activate.bat
```

Install the dependencies needed to run the tests for the model.
```
py -m pip install -r requirements.txt
```

After successfully setting up the virtual environment you can 
now [Create a Key Pair](#create-a-key-pair) needed to run the API and the 
example server.


### Windows Powershell

```
py -m venv .venv
```

Inform PowerShell that you want the current shell process to allow execution
of scripts. Otherwise, you'll get an error telling you that it cannot execute
the script in the next step
```
Set-ExecutionPolicy Unrestricted -Scope Process -Force
```

Activate the virtual environment. This should change the prompt in some manner 
so that it displays the string `.venv` to remind you that the virtual 
environment has been activated.
```
.venv\Scripts\Activate.ps1
```

Install the dependencies needed to run the tests for the model.
```
py -m pip install -r requirements.txt
```

After successfully setting up the virtual environment you can 
now [Create a Key Pair](#create-a-key-pair) needed to run the API and the 
example server.


Create a Key Pair
-----------------

### Mac OS X

Run the following command to generate the key pair.
```bash
python3 -m gameauth
```

You will be asked to provide a passphrase used to encrypt the private key.
For our purposes here you can simply use `secret` as the passphrase. If you
wish to use another secret, you might also want to update 
`api/config.py` and `docker-compose.yml` to match.

After successfully creating the key pair, you can now go to either of these
sections.

* [Running the Server](#running-the-server)
* [Running the Client UI](#running-the-client-ui)
* [Running Everything](#running-everything)

### Windows Command Prompt or Powershell

Run the following command to generate the key pair.
```bash
py -m gameauth
```

You will be asked to provide a passphrase used to encrypt the private key.
For our purposes here you can simply use `secret` as the passphrase. If you
wish to use another secret, you might also want to update 
`api/config.py` and `docker-compose.yml`to match.

After successfully completing the setup, you can now go to either of these
sections
* [Running the Server](#running-the-server)
* [Running the Client UI](#running-the-client-ui)
* [Running Everything](#running-everything)


Reactivating the Virtual Environment
------------------------------------

### Mac OS X

Activate the virtual environment.
```bash
source .venv/bin/activate
```

### Windows Command Prompt

```
.venv\Scripts\activate.bat
```

### Windows PowerShell

```
Set-ExecutionPolicy Unrestricted -Scope Process -Force
```

Activate the virtual environment.
```
.venv\Scripts\Activate.ps1
```

Running the Server
------------------

### Mac OS X

Set the Python package path. Note that the directory path given here leads
from the current directory to the directory containing the `server` and `gui`
packages.

Run the server
```bash
python3 -m server
```

### Windows Command Prompt

Run the server
```
py -m server
```


### Windows PowerShell

Run the server
```
py -m server
```

Running the Api (uses JsonDatabase - couldn't correctly configure with Mongo)
------------------

### Mac OS X

Run the api
```bash
python3 -m api
```

### Windows Command Prompt

Run the api
```
py -m api
```


### Windows PowerShell

Run the api
```
py -m api
```
Running the Client UI (You will need two client terminals one for each client)
there is also a --url feature to specify url
---------------------

### Mac OS X

Run the client
```bash
python3 -m client
```

### Windows Command Prompt

Run the client
```
py -m client
```


### Windows PowerShell

Run the client
```
py -m client
```

Running Everything
------------------

### Mac OS X

You'll need two terminals. In each terminal, make sure that your shell's 
current directory is the base directory that contains the war folder.

In the first terminal, run Docker Compose to start up all the back end
services.
```bash
docker compose up --build --detach
```

In the second terminal, run the Launcher to create some players and a game
instance and launch the GUI for each player.

```bash
python3 -m client --url https://game-api.localhost.devcom.vt.edu 
```

While running everything, you can watch the logs of game server or the API
using Docker Compose. For example, to follow the log of the game server use:

```
docker compose logs --follow game-server
```

To follow the logs of the API, use `game-api` instead.

Press Ctrl-C to stop following the logs.

After experimenting with the example, you can shut down the stack for the
game using

```
docker compose down
```


### Windows Command Prompt

In the first window, run Docker Compose to start up all the back end
services.
```
docker compose up --build --detach
```

In the second window, run the Launcher to create some players and a game
instance and launch the GUI for each player.

```
py -m launcher --url https://game-api.localhost.devcom.vt.edu alice bob mallory
```

While running everything, you can watch the logs of game server or the API
using Docker Compose. For example, to follow the log of the game server use:

```
docker compose logs --follow game-server
```

To follow the logs of the API, use `game-api` instead.

Press Ctrl-C to stop following the logs.

After experimenting with the example, you can shut down the stack for the
game using

```
docker compose down
```


### Windows PowerShell

In the first window, run Docker Compose to start up all the back end
services.
```
docker compose up --build --detach
```

In the second window, run the Launcher to create some players and a game
instance and launch the GUI for each player.

```
py -m launcher --url https://game-api.localhost.devcom.vt.edu alice bob mallory
```

While running everything, you can watch the logs of game server or the API
using Docker Compose. For example, to follow the log of the game server use:

```
docker compose logs --follow game-server
```

To follow the logs of the API, use `game-api` instead.

Press Ctrl-C to stop following the logs.

After experimenting with the example, you can shut down the stack for the
game using

```
docker compose down
```


To run docker Images:
------------------------------

api image 
```
docker pull jlkedda110/war_api
```
server image
```
docker pull jlkedda110/war_server
```
