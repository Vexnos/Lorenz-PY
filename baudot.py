"""
======================
   file: baudot.py
project: Lorenz Cipher
 author: Vexnos
   date: 2026-10-23
======================
"""
# ------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------

import json5
from enum import Enum

# ------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------
class ShiftState(Enum):
    """ Baudot Machine Shift State Enum """
    LETTERS = "11111"
    FIGURES = "11011"

class BaudotMachine:
    """A Baudot Machine to convert plaintext into Baudot-Murray 5bit 
    binary according to ITA2.

    Attributes:
        ITA2_LETTERS (dict[str, str]): Code table for letters
        ITA2_FIGURES (dict[str, str]): Code table for figures
    """
    ITA2_LETTERS: dict[str, str]
    ITA2_FIGURES: dict[str, str]

    def __init__(self) -> None:
        self.import_ITA2()

    # --------------------------------------------------------------------
    # Import ITA2 Table from Json5
    # --------------------------------------------------------------------
    def import_ITA2(self) -> None:
        """ Import ITA2 Code Tables """
        with open('baudot_ITA2.json5', 'r') as file:
            contents: dict = json5.load(file)

        self.ITA2_LETTERS = {
            key: value[0] for key, value in contents["ITA2"].items()
        }

        self.ITA2_FIGURES = {
            key: value[1] for key, value in contents["ITA2"].items()
        }

    # --------------------------------------------------------------------
    # Reverse a Dictionary
    # --------------------------------------------------------------------
    def reverse_dict(self, table: dict) -> dict[str, str]:
        """ Reverse a table """
        return {value: key for key, value in table.items()}

    # --------------------------------------------------------------------
    # Encode
    # --------------------------------------------------------------------
    def encode(self, message) -> str:
        """Encode plaintext into 5bit Baudot 

        Reverses ITA2 dictionaries for encoding, checks what dictionary a
        char is in and sets the required shift state to access the 
        equivalent 5bit representation.

        Args:
            message (str): Plaintext to encode

        Returns:
            str: Encoded message
        """
        result = []
        letters_reversed = self.reverse_dict(self.ITA2_LETTERS)
        figures_reversed = self.reverse_dict(self.ITA2_FIGURES)

        current_shift = ShiftState.LETTERS

        for char in message:
            # Char is in both dictionaries, no need to change shift state
            if char in letters_reversed and char in figures_reversed:
                encoded_char = letters_reversed[char]
                required_shift = current_shift
            # Char is in letters
            elif char in letters_reversed:
                encoded_char = letters_reversed[char]
                required_shift = ShiftState.LETTERS
            # Char is in figures
            elif char in figures_reversed:
                encoded_char = figures_reversed[char]
                required_shift = ShiftState.FIGURES
            else:
                print(
                    f'WARNING: {char!r} is not supported and will be '
                    'ignored!'
                )
                continue

            # Check if shift needs to be inserted
            if current_shift != required_shift:
                if required_shift == ShiftState.LETTERS:
                    result.append(ShiftState.LETTERS.value)
                else:
                    result.append(ShiftState.FIGURES.value)

                current_shift = required_shift

            result.append(encoded_char)

        return ' '.join(result)

    # --------------------------------------------------------------------
    # Decode
    # --------------------------------------------------------------------
    def decode(self, message: str) -> str:
        """Decode 5bit Baudot into plaintext

        Iterate over each bit segment and return equivalent char or figure.

        Args:
            message (str): 5bit Baudot Message

        Returns:
            str: Decoded plaintext
        """
        result = []

        current_shift = ShiftState.LETTERS

        for bits in message.split():
            # Check shift state
            if bits == ShiftState.LETTERS.value:
                current_shift = ShiftState.LETTERS
                continue
            elif bits == ShiftState.FIGURES.value:
                current_shift = ShiftState.FIGURES
                continue

            # Decode char into plaintext
            if current_shift == ShiftState.LETTERS:
                result.append(self.ITA2_LETTERS[bits])
            elif current_shift == ShiftState.FIGURES:
                result.append(self.ITA2_FIGURES[bits])
            else:
                print(f'WARNING: {bits!r} was not found and will be ignored')

        return ''.join(result)

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------
def main() -> None:
    """ Main Function """
    baudot = BaudotMachine()

    message: str = input('Message: ').upper()
    decrypt: bool = input('Decrypt? (y/N): ').lower().startswith('y')

    if not decrypt:
        print(baudot.encode(message))
    else:
        print(baudot.decode(message))

# ------------------------------------------------------------------------
# Main Routine
# ------------------------------------------------------------------------
if __name__ == '__main__':
    main()