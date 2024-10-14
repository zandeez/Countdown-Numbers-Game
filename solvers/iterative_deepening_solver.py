from collections import namedtuple
from itertools import cycle, islice, product

from typing import List, Iterator

from nodes import Node, OperatorNode, NumberNode, Operator
from solvers import Solver

# NamedTuple are more readable than unnamed tuples but don't have unnecessary overheads associated with a full class.
QueueItem = namedtuple('QueueItem', ['node', 'remaining'])


class NextStateGeneratorVisitor:
    def __init__(self, current_state: QueueItem, depth_first: bool = False):
        self.current_state: QueueItem = current_state
        self.depth_first = depth_first
        self.current_leaf: int = 0
        self.check_leaf: int = 0

    def generate_next_states(self) -> Iterator[QueueItem]:
        if self.current_state.remaining:
            for i in range(6 - len(self.current_state.remaining)):
                self.current_leaf = 0
                self.check_leaf = i
                return self.visit(self.current_state.node)

    def visit_number(self, node: NumberNode) -> Iterator[QueueItem]:
        if self.check_leaf == self.current_leaf:
            remaining_cycle = cycle(self.current_state.remaining)
            for i in range(len(self.current_state.remaining)):
                next_number = next(remaining_cycle)
                next_remaining = list(reversed(sorted(islice(remaining_cycle, len(self.current_state.remaining) - 1))))
                operators = list(Operator)
                if self.depth_first:
                    next_remaining = next_remaining[::-1]
                    operators = operators[::-1]
                for operator in operators:
                    yield QueueItem(OperatorNode(operator, NumberNode(next_number), node.clone()),
                                    next_remaining)
                    if not operator.commutative:
                        yield QueueItem(
                            OperatorNode(operator, node.clone(), NumberNode(next_number)),
                            next_remaining)
                next(remaining_cycle)
        else:
            yield QueueItem(NumberNode(node.value), self.current_state.remaining)
        self.current_leaf += 1

    def visit_operator(self, node: OperatorNode) -> Iterator[QueueItem]:
        for left, right in product(self.visit(node.left), self.visit(node.right)):
            if len(left.remaining) < len(right.remaining):
                remaining = left.remaining
            else:
                remaining = right.remaining
            yield QueueItem(OperatorNode(node.operator, left.node.clone(), right.node.clone()), remaining)

    def visit(self, node: Node) -> Iterator[QueueItem]:
        if isinstance(node, NumberNode):
            return self.visit_number(node)
        elif isinstance(node, OperatorNode):
            return self.visit_operator(node)


class IterativeDeepeningSolver(Solver):
    """
    This class solves using a breadth-first search using iterative deepening to find a solution. Starting with a queue
    of solutions which are just the base number, generate new states by pushing up a new operator with a new other value
    from the list of remaining numbers. One you have found a solution, return it. If you don't find a solution, return
    the closest result found.
    """

    def solve(self, depth_first: bool = False) -> Node:
        # The list of unevaluated states
        state_queue: List[QueueItem] = []
        # The best known state found so far
        best_state: Node
        # The distance of the best state from the target answer
        best_dist: int = 1000
        # Set of already evaluated states so equivalent states can be skipped
        visited = set()

        # Fancy way of rotating the numbers so that I can generate the initial states. This iterator repeats the list of
        # numbers infinitely
        number_cycle = cycle(reversed(sorted(self._game.numbers)))

        # Build the initial state queue, this will be with a single NumberNode at the root of the tree for each number
        # in the list.
        for _ in range(len(self._game.numbers)):
            # Create the number node using the next number in the cycle
            node = NumberNode(next(number_cycle))
            # Take the next 5 items to be the unused numbers list for this state
            rest = list(sorted(islice(number_cycle, 5)))
            # Advance the cycle, so the next iteration of this loop starts at the next number
            next(number_cycle)
            # Add the item to the queue.
            state_queue.append(QueueItem(node, rest))

        # Keep looking for solutions while there are still unevaluated states to explore.
        while state_queue:
            if depth_first:
                # Remove the last state from the queue
                current_state = state_queue.pop()
            else:
                # Remove the next item from the queue
                current_state = state_queue.pop(0)
            # See if the string representation of this candidate solution has been seen before. We can assume that if
            # the string representation is equal that the solutions can be considered identical. If we've seen it before
            # just skip to the next one.
            if current_state.node in visited:
                continue
            # This is a new candidate solution. We now store this an evaluated one.
            visited.add(current_state.node)

            # Run the calculation. The error handler weeds out invalid states, for example, divisions with remainders or
            # subtractions that go negative.
            try:
                result = current_state.node.eval()
            except ValueError:
                pass
            else:
                # If we've found an exact solution, return it immediately.
                if result == self._game.target:
                    return current_state.node
                # If not, see if this is a new closest solution, and record it.
                elif (dist := abs(result - self._game.target)) < best_dist:
                    best_state = current_state.node
                    best_dist = dist

            # Generate next states. This will be adding each of the next numbers with each of the next operators.
            generator = NextStateGeneratorVisitor(current_state, depth_first)
            if new_states := generator.generate_next_states():
                state_queue += new_states

        return best_state
