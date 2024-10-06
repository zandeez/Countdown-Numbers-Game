from nodes import Operator, OperatorNode, NumberNode
from game import CountdownGame

if __name__ == '__main__':
    example = OperatorNode(Operator.TIMES, OperatorNode(Operator.MINUS, NumberNode(5), NumberNode(3)), NumberNode(7))
    print(f"{str(example)} = {example.eval()}")

    fixed = CountdownGame([1, 10, 25, 50, 4, 4], 325)
    random = CountdownGame.generate()
    print(str(fixed))
    print(str(random))
