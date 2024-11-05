from collections import defaultdict
from functools import lru_cache
from typing import List

"""
Represents the given keypad internally as a 2D non-jagged array.
"""
class Keypad:
    def __init__(self):
        self._keypad = [['A', 'B', 'C', 'D', 'E'],
                       ['F', 'G', 'H', 'I', 'J'],
                       ['K', 'L', 'M', 'N', 'O'],
                       [None, '1', '2', '3', None]]

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


"""
Solution finder to find the valid knight moves for a given keypad and sequence_length/max_vowel constraints
"""
class KeypadSequenceFinder:
    _vowels = {'A', 'E', 'I', 'O'}
    _knight_moves = [
        (-2, -1), (-2, 1), (2, -1), (2, 1),  # two vertical, one horizontal
        (-1, -2), (1, -2), (-1, 2), (1, 2)  # two horizontal, one vertical
    ]

    def __init__(self, keypad: Keypad, sequence_length: int = 10, max_vowels: int = 2):
        self.max_vowels = max_vowels
        self.sequence_length = sequence_length
        self.keypad = keypad
        self._valid_next_moves = defaultdict(set)


    """
    This method takes in a key and returns the possible list of valid next keys, according to the allowed knight_moves
    It lazily builds up a cache as it is called so performance will improve until all keys are passed in at least once.
    """
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

    """
    A recursive method to get the total number of sequences that are possible within the bounds of MAX_VOWELS and DESIRED_SEQ_LENGTH.
    This method uses a cache (memoisation) to reduce the number of repeated recursive calls. 
    """
    def get_sequence_count(self, key: str, length: int, num_vowels: int, keys: List[str]) -> int:
        # if the sequence length is sequence_length, the sequence is valid, return 1
        if length == self.sequence_length:
            print(keys)
            return 1

        total = 0
        valid_next_keys = self.get_valid_next_moves(key)
        for next_key in valid_next_keys:
            if next_key in self._vowels:
                if num_vowels < self.max_vowels:  # Only recurse if we have not met our vowel limit
                    total += self.get_sequence_count(next_key, length + 1, num_vowels + 1, keys + [next_key])
            else:
                total += self.get_sequence_count(next_key, length + 1, num_vowels, keys + [next_key])
        return total

    """
    Get the total number of possible combinations for all valid initial key presses
    """
    def get_total_count(self):
        return sum(self.get_sequence_count(key, length=1,
                                           num_vowels=1 if key in self._vowels else 0,
                                           keys=[])
                   for key in self.keypad.get_keys())

    """
    Check whether a given sequence is valid
    """
    def validate_sequence(self, sequence: List[str]):
        if len(sequence) != self.sequence_length:
            raise ValueError(f"Invalid sequence length for keypad: {sequence}")

        if len([c for c in sequence if c in self._vowels]) > self.max_vowels:
            raise ValueError("Too many vowels in sequence: {sequence}".format(sequence=sequence))

        for i in range(1, len(sequence)):
            next_moves = self.get_valid_next_moves(sequence[i-1])
            if sequence[i] in next_moves:
                continue
            else:
                print(f"Invalid move {sequence[i]}({i}) from {sequence[i-1]}({i-1}). Should be one of {next_moves}")
                return False
        return True


if __name__ == '__main__':
    kp = Keypad()
    max_seq_length = 10
    max_vowels = 2
    finder = KeypadSequenceFinder(kp, sequence_length=max_seq_length, max_vowels=max_vowels)
    print(f"Total number of valid sequences of length: {max_seq_length} "
          f"and max_num_vowels: {max_vowels} "
          f"is {finder.get_total_count():,}")
