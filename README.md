# Tic Tac Toe

Tic Tac Toe project for my COSC-1436 class. Provides a graphical interface to the user and a computer opponent.

## Getting Started

All you need to do is download and run [tictactoe-build.py](tictactoe-build.py):

    python ./tictactoe-build.py

The tictactoe-build.py script contains all the source code in one file. If for any reason this isn't working you can also just run the script from the full source code:

    python ./tictactoe.py

### Prerequisites

I haven't extensively tested python versions so this is really just an educated guess based on ZyBooks' reported version.
- [Python 3.8.10+](https://www.python.org/downloads/release/python-3810/)

## Why BitBoards?

I was inspired by a video by Sebastian Lague: [**Coding Adventure: Making a Better Chess Bot**](https://www.youtube.com/watch?v=_vqlIPDR2TU&t=1175s).

Using BitBoards for Tic Tac Toe is definitely overkill, but I though it would be a fun way to introduce myself to the concept.

I included an explination of the main bitboard and its related masks in the Game class in [Game.py](src/game.py)

## Computer Opponent

There is an optional computer opponent that can be played against.

### Computer Levels

Valid computer levels are from 0 to 8. Unfortunately the computer levels are not linear with difficulty. It only controls the depth the computer evaluates.

- For level = 0, the computer randomly selects a move.
- For any level > 0, the computer recursively checks and simulates moves from both players until it reaches a depth greater than the desired computer level.

### Move Selection For Level > 0

The computer recursively checks each possible move, assuming optimal play from either side.

When the computer checks any move, it first evaluates the board after the move is played and performs one of the following:

- Returns a score of 10, if the computer itself won.
- Returns a score of -10, if the computer itself loses.
- Returns a score of 0, if neither player wins or there is a tie.

If the computer hits its depth limit, it has trouble picking a move. This often causes the first move it checks to be played which significantly reduced move quality. To alleviate this, the computer then checks if the move blocks the other player from winning. If the move does block a win, it slightly incentivises this move with a score of 5.