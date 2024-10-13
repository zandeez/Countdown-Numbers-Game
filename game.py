from collections import defaultdict
from typing import List, Dict, Optional
import random


class CountdownGame:
    """
    A representation of a game state, that is the numbers available for use, and the target number. This class is likely
    not really required and a dataclass, 2-tuple or named tuple would probably suffice in its place, but this class
    gives a clear separation of code for generating a game state. You can either create an instance directly using the
    constructor, supplying a predefined number list and target, or use the generate static method to set up a random
    game, optionally specifying how many large numbers. The constructor also validates the input.
    """

    # Numbers for this game
    _numbers: List[int]
    # The target number for the game
    _target: int

    # A list of big numbers, one of each.
    BIG_NUMBERS: List[int] = [25, 50, 75, 100]
    # A list of small numbers, two of each.
    SMALL_NUMBERS: List[int] = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]
    # A set of all valid numbers, for validity checking.
    VALID_NUMBERS = set(BIG_NUMBERS + SMALL_NUMBERS)

    def __init__(self, numbers: List[int], target: int):
        """
        Create a new CountdownGame instance with a predetermined list of numbers and a target number.
        :param numbers: The list of numbers for the game
        :param target: The target number to calculate.
        """
        # Target number should be between 100 and 999 inclusive
        if target < 100 or target > 999:
            raise ValueError("Target must be between 100 and 999 inclusive")

        # There should be exactly 6 numbers
        if len(numbers) != 6:
            raise ValueError(
                f"Please specify exactly 6 numbers from the set {sorted(CountdownGame.VALID_NUMBERS)}. Big numbers can be specified ones only, Small numbers can be specified twice.")

        # Check the number list is valid. To do this, we'll loop over the numbers provided and count them into a
        # dictionary. Using defaultdict to automatically initialise all values to 0.
        numbers.sort()
        number_frequencies: Dict[int, int] = defaultdict(lambda: 0)
        for number in numbers:
            # Check the numbers are valid according to the list of valid numbers.
            if number not in CountdownGame.VALID_NUMBERS:
                raise ValueError(
                    f"Number {number} is not a valid number. Valid numbers are {sorted(CountdownGame.VALID_NUMBERS)}")
            # Big numbers can only appear once. If the number has appeared before, raise an error.
            elif number > 10 and number_frequencies[number] == 1:
                raise ValueError(f"Small numbers can be specified at most twice. ({number})")
            # Small numbers can only appear twice. If the number has already been seen twice, raise an error.
            elif number <= 10 and number_frequencies[number] == 2:
                raise ValueError(f"Big numbers can be specified at most once. ({number})")
            # If none of the above conditions are met, then we're good to increase the counter for this number.
            else:
                number_frequencies[number] += 1

        # At this stage the game inputs have been validated, store them.
        self._numbers = numbers
        self._target = target

    @staticmethod
    def generate(large_numbers: Optional[int] = None):
        """
        Generates a random countdown game by randomly selecting the numbers and target number.
        :param large_numbers: optionally, the number of large numbers that should be selected
        :return: a new instance of CountdownGame with randomly selected numbers and target number.
        """
        # Check the value of large_numbers is valid, if present. Otherwise, randomly select the number of large numbers
        if large_numbers and (large_numbers < 0 or large_numbers > 4):
            raise ValueError("The number of large numbers must be between 0 and 4 inclusive.")
        elif not large_numbers:
            large_numbers = random.randint(0, 4)

        # Shuffle the number card decks each time.
        random.shuffle(CountdownGame.SMALL_NUMBERS)
        random.shuffle(CountdownGame.BIG_NUMBERS)
        # Generate the target number.
        target = random.randint(100, 999)

        # Create the list of numbers by array slicing, we want the specified number of large numbers, and the remaining
        # from the 6 as small numbers. The number decks are pre-shuffled above so this should be different each time.
        numbers = CountdownGame.SMALL_NUMBERS[0: 6 - large_numbers] + CountdownGame.BIG_NUMBERS[0:large_numbers]
        return CountdownGame(numbers, target)

    @property
    def numbers(self) -> List[int]:
        """
        :return: The list of numbers available for use.
        """
        return self._numbers

    @property
    def target(self) -> int:
        """
        :return: The target number to calculate.
        """
        return self._target

    def __str__(self):
        return f"Numbers: {", ".join([str(number) for number in self.numbers])}, Target: {str(self.target)}"
