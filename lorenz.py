"""

================================
   file: lorenz.py
project: Lorenz Cipher in Python
 author: Vexnos
   date: 2026-10-23
================================

"""
# ------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------

import baudot
from wheels import Wheel

# ------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------
def xor_bits(bits: str) -> str:
    bit = int(bits, 2)
    result = bit ^ 0b10101
    return f'{result:05b}'

def xor_message(message: str) -> str:
    result: list[str] = []
    for bits in message.split():
        result.append(xor_bits(bits))
    return ' '.join(result)

def main() -> None:
    ITA2_LETTERS, ITA2_FIGURES = baudot.import_ITA2()
    
    message: str = input('Message: ').upper()

    message = baudot.encode(ITA2_LETTERS, ITA2_FIGURES, message)

    message = xor_message(message)

    print(baudot.decode(ITA2_LETTERS, ITA2_FIGURES, message))

# ------------------------------------------------------------------------
# Main Routine
# ------------------------------------------------------------------------
if __name__ == '__main__':
    main()