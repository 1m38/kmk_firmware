print("Starting")

import board

# from kmk.kmk_keyboard import KMKKeyboard
from duplex_matrix import KMKKeyboardDuplexMatrix
from kmk.keys import KC
from kmk.matrix import DiodeOrientation

# Duplex Matrix

keyboard = KMKKeyboardDuplexMatrix()
keyboard.debug_enabled = True

keyboard.cols_pins = [
    (board.GP3, board.GP4),
    (board.GP3, board.GP4)
]
keyboard.rows_pins = [
    (board.GP6, board.GP7),
    (board.GP6, board.GP7)
]
# keyboard.diode_orientation = DiodeOrientation.COL2ROW
keyboard.diode_orientations = [
    DiodeOrientation.COL2ROW,
    DiodeOrientation.ROW2COL
]

keyboard.keymap = [
    [
        KC.A, KC.B,
        KC.C, KC.D,
        KC.E, KC.F,
        KC.G, KC.H
    ]
]

if __name__ == '__main__':
    keyboard.go()
