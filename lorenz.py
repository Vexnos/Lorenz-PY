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

from baudot import BaudotMachine

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
    result = []
    for bits in message.split():
        result.append(xor_bits(bits))
    return ' '.join(result)

def main() -> None:
    baudot = BaudotMachine()
    
    message: str = input('Message: ').upper()

    message = baudot.encode(message)

    message = xor_message(message)

    print(baudot.decode(message))

# ------------------------------------------------------------------------
# Main Routine
# ------------------------------------------------------------------------
if __name__ == '__main__':
    main()