# Professional Skills 1 - Chess

This is the official repository for our chess game.
The main file is the chess program. The idea is to have a beamer above a physical chess board that has 64 light sensors in it (we use LDR sensors). The sensors are protected by a plate running over the entire board and is easily cleanable. The sensors need to be linked to a microcomputer (in our case an orange pi). Once the setup is ready you can launch the program and you can play a game of chess. The game is played between two players, but with extra tweaking you could add a bot. The beamer will display the positions of the pieces that are shown on the computer. This will also ensure that the sensors have enough light on them to notice a change in light levels. The game ends once someone has checkmate or 50 turns have passed.


Required PIP packages: `python-chess`, `requests`, `time`, `wiringpi`, `selenium`. These packages have to be installed for the program to work.
