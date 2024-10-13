from nodes import Operator, OperatorNode, NumberNode
from game import CountdownGame
from solvers.iterative_deepening_solver import IterativeDeepeningSolver

if __name__ == '__main__':
    example = OperatorNode(Operator.TIMES, OperatorNode(Operator.MINUS, NumberNode(5), NumberNode(3)), NumberNode(7))
    print(f"{str(example)} = {example.eval()}")
    print()

    fixed = CountdownGame([1, 10, 25, 50, 4, 4], 325)
    print(str(fixed))
    i = IterativeDeepeningSolver(fixed)
    result = i.solve()
    print(result, "=", result.eval())
    print()

    random = CountdownGame.generate()
    print(str(random))
    j = IterativeDeepeningSolver(random)
    result = j.solve()
    print(result, "=", result.eval())
    print()

