from collections import defaultdict
from functools import lru_cache

"""
Represents the given keypad internally as a 2D non-jagged array.
"""


class Keypad:
    def __init__(self, keypad=[['A', 'B', 'C', 'D', 'E'],
                               ['F', 'G', 'H', 'I', 'J'],
                               ['K', 'L', 'M', 'N', 'O'],
                               [None, '1', '2', '3', None]]):
        self._keypad = keypad

        self._key_positions = dict()

    """
    Returns the character at a particular row/col position, zero-indexed.
    :return None for a position that does not contain a key, otherwise the key at that position
    """

    def get_key(self, row: int, col: int) -> str:
        if row > len(self._keypad) or col >= len(self._keypad[row]):
            raise ValueError(f"Invalid index for keypad: {row}, {col}")
        return self._keypad[row][col]

    """
    Get all the keys that exist on the Keypad
    :return The full list of keys on the keypad
    """

    def get_keys(self):
        return [i for i in [j for sub_list in self._keypad for j in sub_list] if i is not None]

    """
    Get the total number of rows on the Keypad
    :return the number of rows on the keypad
    """

    def get_num_rows(self):
        return len(self._keypad)

    """
    Get the number of columns for a row on the Keypad
    :return the number of columns on the keypad for the given zero-indexed row
    """

    def get_num_cols(self, row: int):
        if row >= len(self._keypad):
            raise ValueError(f"Invalid row for keypad: {row}")
        return len(self._keypad[row])

    """
    This method takes in a key and returns the position on the keypad as a tuple.
    It lazily builds up a cache as it is called so performance will improve until all keys are passed in at least once.
    """

    def get_key_position(self, key: str) -> tuple[int, int]:
        if key in self._key_positions:
            return self._key_positions[key]

        for i in range(self.get_num_rows()):
            for j in range(self.get_num_cols(i)):
                if self.get_key(i, j) == key:
                    self._key_positions[key] = i, j
                    return i, j
        raise ValueError(f"Invalid key {key}")


class Mover:
    def __init__(self, keypad: Keypad):
        self.keypad = keypad
        self._valid_next_moves = defaultdict(set)

    def get_valid_next_moves(self, key: str) -> set[str]:
        pass


class KnightMover(Mover):
    _knight_moves = [
        (-2, -1), (-2, 1), (2, -1), (2, 1),  # two vertical, one horizontal
        (-1, -2), (1, -2), (-1, 2), (1, 2)  # two horizontal, one vertical
    ]

    def __init__(self, keypad: Keypad):
        super().__init__(keypad)

    def get_valid_next_moves(self, key: str) -> set[str]:
        if key in self._valid_next_moves:
            return self._valid_next_moves[key]

        row, col = self.keypad.get_key_position(key)
        for r, c in self._knight_moves:
            new_r, new_c = row + r, col + c
            if (0 <= new_r < self.keypad.get_num_rows()
                    and 0 <= new_c < self.keypad.get_num_cols(new_r)
                    and self.keypad.get_key(new_r, new_c) is not None):
                self._valid_next_moves[key].add(self.keypad.get_key(new_r, new_c))
        return self._valid_next_moves[key]


class BishopMover(Mover):
    _bishop_moves = [(-1, -1), (1, 1), (-1, 1), (1, -1)]

    def __init__(self, keypad: Keypad):
        super().__init__(keypad)

    def get_valid_next_moves(self, key: str) -> set[str]:
        if key in self._valid_next_moves:
            return self._valid_next_moves[key]

        row, col = self.keypad.get_key_position(key)
        for r, c in self._bishop_moves:
            new_r, new_c = row + r, col + c
            while 0 <= new_r < self.keypad.get_num_rows() and 0 <= new_c < self.keypad.get_num_cols(
                    new_r) and self.keypad.get_key(new_r, new_c) is not None:
                self._valid_next_moves[key].add(self.keypad.get_key(new_r, new_c))
                new_r = new_r + r
                new_c = new_c + c

        #
        # for i in range(1, self.keypad.get_num_rows()):
        #     # Positive Slope
        #     if row + i < self.keypad.get_num_rows() and col + i < self.keypad.get_num_cols(row + i) and self.keypad.get_key(row + i, col + i) is not None:
        #         self._valid_next_moves[key].add(self.keypad.get_key(row + i, col + i))
        #     if row - i >= 0 and col - i >= 0 and self.keypad.get_key(row - i, col - i) is not None:
        #         self._valid_next_moves[key].add(self.keypad.get_key(row - i, col - i))
        #     # Negative Slope
        #     if row + i < self.keypad.get_num_rows() and col - i >= 0 and self.keypad.get_key(row + i, col - i) is not None:
        #         self._valid_next_moves[key].add(self.keypad.get_key(row + i, col - i))
        #     if row - i >= 0 and col + i < self.keypad.get_num_cols(row - i) and self.keypad.get_key(row - i, col + i) is not None:
        #         self._valid_next_moves[key].add(self.keypad.get_key(row - i, col + i))

        return self._valid_next_moves[key]


"""
Solution finder to find the valid knight moves for a given keypad and sequence_length/max_vowel constraints
"""


class KeypadSequenceFinder:
    _vowels = {'A', 'E', 'I', 'O'}

    def __init__(self, keypad: Keypad, mover: Mover, sequence_length: int = 10, max_vowels: int = 2):
        self.max_vowels = max_vowels
        self.sequence_length = sequence_length
        self.keypad = keypad
        self.mover = mover

    """
    This method takes in a key and returns the possible list of valid next keys, according to the allowed knight_moves
    It lazily builds up a cache as it is called so performance will improve until all keys are passed in at least once.
    """

    def get_valid_next_moves(self, key: str) -> set[str]:
        return self.mover.get_valid_next_moves(key)

    """
    A recursive method to get the total number of sequences that are possible within the bounds of MAX_VOWELS and DESIRED_SEQ_LENGTH.
    This method uses a cache (memoisation) to reduce the number of repeated recursive calls. 
    """

    @lru_cache(None)
    def get_sequence_count(self, key: str, length: int, num_vowels: int) -> int:
        # if the sequence length is sequence_length, the sequence is valid, return 1
        if length == self.sequence_length:
            return 1

        total = 0
        valid_next_keys = self.get_valid_next_moves(key)
        for next_key in valid_next_keys:
            if next_key in self._vowels:
                if num_vowels < self.max_vowels:  # Only recurse if we have not met our vowel limit
                    total += self.get_sequence_count(next_key, length + 1, num_vowels + 1)
            else:
                total += self.get_sequence_count(next_key, length + 1, num_vowels)
        return total

    """
    Get the total number of possible combinations for all valid initial key presses
    """

    def get_total_count(self):
        return sum(self.get_sequence_count(key, 1, 1 if key in self._vowels else 0) for key in self.keypad.get_keys())


if __name__ == '__main__':
    kp = Keypad()
    max_seq_length = 10
    max_vowels = 2
    mover = BishopMover(kp)
    finder = KeypadSequenceFinder(kp, mover=mover, sequence_length=max_seq_length, max_vowels=max_vowels)
    print(f"Total number of valid sequences of length: {max_seq_length} "
          f"and max_num_vowels: {max_vowels} "
          f"is {finder.get_total_count():,}")
