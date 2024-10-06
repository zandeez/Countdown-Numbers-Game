from game import CountdownGame
from nodes import Node
import abc


class Solver(abc.ABC):
    def __init__(self, game: CountdownGame):
        self._game = game

    @abc.abstractmethod
    def solve(self) -> Node:
        raise NotImplementedError
