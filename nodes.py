from enum import Enum
import abc
import random


class Operator(Enum):
    """
    We use an Enum class here because it restricts possible values. In this case, the four main mathematical operators.
    """
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    DIVIDE = '/'

    @staticmethod
    def random_operator() -> 'Operator':
        """
        Selects a random operator
        :return: the selected random operator
        """
        return random.choice(list(Operator))

    def __str__(self):
        """
        Override the default __str__ method to return the value (the symbol) rather than the name.
        :return: the symbol of the operator
        """
        return self.value


class Node(abc.ABC):
    """
    Abstract Base Class (ABC) for a Node for the binary tree that represents a possible solution. Abstract Base Classes
    allow for polymorphic code to expect certain methods or attributes are available on an object that inherits it.
    ABCs should not be instantiated or used directly. This class says that all inheriting subtypes must have an eval
    method that has no parameters and returns an int, and a clone method that returns a deep copy that of the node.

    An example tree for (5 + 3) * 7 would look like this:

                                           OperatorNode *
                                           /            \
                                         left          right
                                         /                \
                                    OperatorNode +    NumberNode 7
                                    /            \
                                  left          right
                                  /                \
                            NumberNode 5       NumberNode 3
    """

    @abc.abstractmethod
    def eval(self) -> int:
        """
        Calculates the value of the subtree from this point
        :return: the calculated value of the subtree
        """
        raise NotImplementedError

    @abc.abstractmethod
    def clone(self) -> 'Node':
        """
        Returns a deep copy of this node
        :return: a deep copy of this node
        """
        raise NotImplementedError


class NumberNode(Node):
    """
    Represents a number in a solution. This is a leaf node for the solution tree, that is it has no child nodes.
    """

    def __init__(self, value: int):
        """
        Create a new number node with the given value
        :param value: The value of the node
        """
        self.value = value

    def eval(self) -> int:
        """
        Returns the value of the node (no children to calculate)
        :return: the value of the node
        """
        return self.value

    def clone(self) -> 'Node':
        """
        Returns a copy of this node
        :return: return a copy of this node
        """
        return NumberNode(self.value)

    def __str__(self):
        """
        Override the __str__ method to return the numeric value of the node as a string
        :return:
        """
        return str(self.value)


class OperatorNode(Node):
    """
    Represent an operation that operate on two subtrees. This is one of the four main mathematical operators, which is
    then performed on the result of evaluating both subtrees.
    """

    def __init__(self, operator: Operator, left: Node, right: Node):
        """
        Create a new operator node
        :param operator: The operator for this node
        :param left: The left subtree of the operator
        :param right: The right subtree of the operator
        """
        self.operator = operator
        self.left = left
        self.right = right

    def eval(self) -> int:
        """
        Evaluate the result of applying the operator to the results of both subtrees.
        :return: The result of applying the operator to the results of both subtrees.
        :raises: ValueError if there is a division that results in a remainder.
        """
        # Calculate the value of the left and right subtrees
        left, right = self.left.eval(), self.right.eval()
        # Apply the relevant calculation depending on which operator type the node represents
        match self.operator:
            case Operator.PLUS:
                return left + right
            case Operator.MINUS:
                if left < right:
                    ValueError("No stage can be negative.")
                return left - right
            case Operator.TIMES:
                return left * right
            case Operator.DIVIDE:
                # Ensure the division does not leave a remainder as this isn't allowed in countdown rules.
                if left % right == 0:
                    return left // right
                raise ValueError("Division leaves a remainder")

    def clone(self) -> 'Node':
        """
        Returns a deep copy of this node
        :return: a deep copy of this node
        """
        return OperatorNode(self.operator, self.left.clone(), self.right.clone())

    @property
    def precedence(self) -> int:
        """
        The precedence of the operator according to BODMAS rules, multiply and divide should apply before plus and minus
        unless the plus or minus themselves are inside brackets. This is used for formatting the string output.
        :return: the precedence of the operator according to BODMAS rules.
        """
        if self.operator == Operator.TIMES or self.operator == Operator.DIVIDE:
            return 2
        return 1

    @property
    def commutative(self) -> bool:
        """
        Indicates whether this node is commutative or not, where the order of the operands affects the result of the
        calculation. Plus and times are commutative, but minus and divide are not.
        :return: True if the operator is commutative, False otherwise.
        """
        return self.operator == Operator.PLUS or self.operator == Operator.TIMES

    def _subtree_string(self, node: Node) -> str:
        """
        A string representation of the given subtree relative to this node, adding brackets if required by BODMAS rules.
        :param node: The subtree to generate the string representation of.
        :return: the string representation of the subtree relative to this node.
        """
        if isinstance(node, OperatorNode) and node.precedence < self.precedence:
            return f"({str(node)})"
        else:
            return str(node)

    def __str__(self):
        """
        A string representation of this subtree, applying brackets if it is required by BODMAS rules.
        :return: string representation of this subtree.
        """
        return f"{self._subtree_string(self.left)} {str(self.operator)} {self._subtree_string(self.right)}"
