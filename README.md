# Countdown Numbers Game

The Countdown Numbers Game is a time-limited aritmetic problem featured on the UK Channel 4 Game Show 'Countdown'.
[https://en.wikipedia.org/wiki/Countdown_(game_show)#Numbers_Round]()

I have built this as a demonstration for anyone interested and tried to use varied techniques.

## Layout of the Repository

The top level contains a "main.py" script that runs a few basic tests and a couple example solvers (once implemented).

game.py contains a single class, representing a game with 6 selected numbers and the target number, and tools for
generating a game at random.

nodes.py contains classes to represent a candidate solution as a binary tree of operators and numbers, with methods for
recursively calculating the total value and a string representation, including parenthesis where necessary.

The solvers directory includes a base Solver class and some example algorithmic solvers.
