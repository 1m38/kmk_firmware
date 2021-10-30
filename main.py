print("Starting")

import board

# from kmk.kmk_keyboard import KMKKeyboard
from duplex_matrix import KMKKeyboardDuplexMatrix
from kmk.keys import KC

keyboard = KMKKeyboardDuplexMatrix()
keyboard.debug_enabled = True

keyboard.col_pins = (board.GP3, board.GP4)
keyboard.row_pins = (board.GP6, board.GP7)

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
