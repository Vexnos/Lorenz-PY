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
import sys
import json5
from wheels import Wheel

# ------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------
class SZ42:
    CHI_WHEELS: list[Wheel] = []
    PSI_WHEELS: list[Wheel] = []
    MOTOR_WHEELS: list[Wheel] = []

    def __init__(
        self, 
        CHI_WHEELS: list[dict],
        PSI_WHEELS: list[dict],
        MOTOR_WHEELS: list[dict]
    ) -> None:
        for wheel in CHI_WHEELS:
            self.CHI_WHEELS.append(
                Wheel(wheel['teeth'], wheel['position'], wheel['cams'])
            )

        for wheel in PSI_WHEELS:
            self.PSI_WHEELS.append(
                Wheel(wheel['teeth'], wheel['position'], wheel['cams'])
            )

        for wheel in MOTOR_WHEELS:
            self.MOTOR_WHEELS.append(
                Wheel(wheel['teeth'], wheel['position'], wheel['cams'])
            )
        
        try:
            self.validate_wheels()
        except ValueError as e:
            print(f'Application Error: {e}', file=sys.stderr)
            sys.exit(1)

    def rotate_wheels(self) -> None:
        for wheel in self.CHI_WHEELS:
            wheel.rotate()

        if self.MOTOR_WHEELS[0].get_cam_position() == 1:
            self.MOTOR_WHEELS[1].rotate()
        self.MOTOR_WHEELS[0].rotate()

        if self.MOTOR_WHEELS[1].get_cam_position() == 1:
            for wheel in self.PSI_WHEELS:
                wheel.rotate()

    def gen_xor_bits(self) -> int:
        result: list[int] = []
        for i in range(len(self.CHI_WHEELS)):
            result.append(
                self.CHI_WHEELS[i].get_cam_position() ^ self.PSI_WHEELS[i].get_cam_position()
            )

        result_str = ''.join(str(r) for r in result)
        return int(result_str, 2)

    def xor_bits(self, bits: str) -> str:
        bit = int(bits, 2)
        self.rotate_wheels()
        xor_bit = self.gen_xor_bits()
        result = bit ^ xor_bit
        return f'{result:05b}'

    def xor_message(self, message: str) -> str:
        result: list[str] = []
        for bits in message.split():
            result.append(self.xor_bits(bits))
        return ' '.join(result)

    def validate_wheels(self) -> None:
        if len(self.CHI_WHEELS) != 5:
            raise ValueError('Invalid amount of Chi Wheels specified.')
        if len(self.PSI_WHEELS) != 5:
            raise ValueError('Invalid amount of Psi Wheels specified.')
        if len(self.MOTOR_WHEELS) != 2:
            raise ValueError('Invalid amount of Motor Wheels specified.')

    def export_wheels(self) -> None:
        chi_wheels: list[dict] = []
        psi_wheels: list[dict] = []
        motor_wheels: list[dict] = []
        for wheel in self.CHI_WHEELS:
            chi_wheels.append(wheel.export_wheel())
        for wheel in self.PSI_WHEELS:
            psi_wheels.append(wheel.export_wheel())
        for wheel in self.MOTOR_WHEELS:
            motor_wheels.append(wheel.export_wheel())

        with open('wheels.json5', 'w') as file:
            json5.dump(
                {
                    'CHI': chi_wheels,
                    'PSI': psi_wheels,
                    'MOTOR': motor_wheels
                },
                file,
                indent=4
            )

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------
def import_wheels() -> tuple:
    with open('wheels.json5', 'r') as file:
        contents = json5.load(file)
    return contents['CHI'], contents['PSI'], contents['MOTOR']

def main() -> None:
    chi, psi, motor = import_wheels()

    lorenz = SZ42(chi, psi, motor)

    ITA2_LETTERS, ITA2_FIGURES = baudot.import_ITA2()
    message: str = input('Message: ').upper()
    message = baudot.encode(ITA2_LETTERS, ITA2_FIGURES, message)
    print(lorenz.xor_message(message))
    # print(baudot.decode(ITA2_LETTERS, ITA2_FIGURES, message))

    # lorenz.export_wheels()

# ------------------------------------------------------------------------
# Main Routine
# ------------------------------------------------------------------------
if __name__ == '__main__':
    main()