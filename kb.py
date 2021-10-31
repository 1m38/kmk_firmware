import board
from duplex_matrix import KMKKeyboardDuplexMatrix
from kmk.keys import KC

class KMKKeyboard(KMKKeyboardDuplexMatrix):
    col_pins = (
        board.D0,
        board.D1,
        board.D28,
        board.D27,
        board.D26,
        board.D22,
        board.D20,
    )
    row_pins = (board.D4, board.D5, board.D6, board.D7)

# Encoder push buttons are handled by keymap
encoder_pins = (
    (board.D23, board.D21, None, False),
    (board.D8, board.D9, None, False)
)

rgb_pixel_pin = board.D29

def layout(
         L01, L02, L03, L04, L05,             R05, R04, R03, R02, R01,
    L10, L11, L12, L13, L14, L15, L16,   R16, R15, R14, R13, R12, R11, R10,
    L20, L21, L22, L23, L24, L25, L26,   R26, R25, R24, R23, R22, R21, R20,
                        L34, L35, L36,   R36, R35, R34,
                             L45,             R45
):
    return [
        KC.NO, L01, L02, L03, L04, L05, KC.NO,
        L10, L11, L12, L13, L14, L15, L16,
        L20, L21, L22, L23, L24, L25, L26,
        KC.NO, KC.NO, KC.NO, L45, L34, L35, L36,
        KC.NO, R01, R02, R03, R04, R05, KC.NO,
        R10, R11, R12, R13, R14, R15, R16,
        R20, R21, R22, R23, R24, R25, R26,
        KC.NO, KC.NO, KC.NO, R45, R34, R35, R36
    ]
