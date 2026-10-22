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

# ------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------
class BaudotMachine:
    """A Baudot Machine to convert plaintext into Baudot-Murray 5bit 
    binary according to ITA2.

    Attributes:
        ITA2_LETTERS (dict[str, str]): Code table for letters
        ITA2_FIGURES (dict[str, str]): Code table for figures
        LETTERS (str): Shift to letters
        FIGURES (str): Shift to figures
    """
    ITA2_LETTERS: dict[str, str]
    ITA2_FIGURES: dict[str, str]
    LETTERS: str
    FIGURES: str

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

        self.LETTERS = contents["LETTERS"]
        self.FIGURES = contents["FIGURES"]

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
        result = []
        letters_reversed = self.reverse_dict(self.ITA2_LETTERS)
        figures_reversed = self.reverse_dict(self.ITA2_FIGURES)

        for char in message:
            if char in letters_reversed:
                result.append(letters_reversed[char])
            elif char in figures_reversed:
                result.append(figures_reversed[char])
            else:
                print(
                    f'WARNING: {char!r} is not supported and will be' 
                    ' ignored.'
                )

        return ' '.join(result)

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------
def main() -> None:
    baudot = BaudotMachine()

    message: str = input('Message: ').upper()

    print(baudot.encode(message))

# ------------------------------------------------------------------------
# Main Routine
# ------------------------------------------------------------------------
if __name__ == '__main__':
    main()