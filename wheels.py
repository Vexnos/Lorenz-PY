"""

=============================
   file: wheels.py
project: Lorenz Cipher Wheels
 author: Vexnos
   date: 2026-10-27
=============================

"""

from random import randint

# ------------------------------------------------------------------------
# Chi & Psi Wheels
# -----------------------------------------------------------------------
class Wheel:
    teeth: int
    position: int

    def __init__(
        self, 
        teeth: int, 
        position: int, 
        cams: list[int] | None = None
    ) -> None:
        self.teeth = teeth
        self.position = position % teeth
        self.cams = cams if cams is not None else self.generate_cams()

    def get_position(self) -> int:
        return self.position
    
    def get_cams(self) -> list[int]:
        return self.cams

    def get_cam_position(self) -> int:
        return self.cams[(self.position % self.teeth)]

    def rotate(self, n: int = 1) -> None:
        self.position += (n % self.teeth)

    def generate_cams(self) -> list[int]:
        result: list[int] = []
        for _ in range(self.teeth):
            result.append(randint(0, 1))
        return result

    def export_wheel(self) -> dict:
        return {
            'teeth': self.teeth,
            'position': self.position,
            'cams': self.cams
        }
        
# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------
def main() -> None:
    print('Hello World!')

# ------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------
if __name__ == '__main__':
    main()