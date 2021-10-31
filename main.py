print("Starting")

import board

from kb import KMKKeyboard, layout
from kmk.keys import KC
import keys_jp as JP
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from kmk.modules.encoder import EncoderHandler
from kmk.modules.mouse_keys import MouseKeys
from kmk.extensions.rgb import RGB
from kb import encoder_pins, rgb_pixel_pin

keyboard = KMKKeyboard()
keyboard.debug_enabled = True

layers_mod = Layers()
keyboard.modules.append(layers_mod)
modtap_mod = ModTap()
keyboard.modules.append(modtap_mod)
# encoder_handler = EncoderHandler()
# encoder_handler.pins = encoder_pins
# keyboard.modules.append(encoder_handler)
# mousekeys_mod = MouseKeys()
# keyboard.modules.append(mousekeys_mod)
rgb_ext = RGB(pixel_pin=rgb_pixel_pin, num_pixels=14)
keyboard.extensions.append(rgb_ext)


class Layer:
    # Qwerty = 0
    # Eucalyn = 1
    # Raise = 2
    # Lower = 3
    # Adjust = 4
    Eucalyn = 0
    Raise = 1
    Lower = 2
    Adjust = 3


_______ = KC.TRNS
XXXXXXX = KC.NO
G = lambda kc: KC.LGUI(kc)
R_HENK = KC.LT(Layer.Raise, KC.HENK)
L_MHEN = KC.LT(Layer.Lower, KC.MHEN)
ADJUST = KC.MO(Layer.Adjust)
ALT_ESC = KC.MT(KC.ESC, KC.LALT)
RGB_TOG = KC.RGB_TOG
# MB_BTN1 = KC.MB_LMB
# MB_BTN2 = KC.MB_RMB
# MB_BTN3 = KC.MB_MMB
MB_BTN1 = XXXXXXX
MB_BTN2 = XXXXXXX
MB_BTN3 = XXXXXXX
RGB_HUI = KC.RGB_HUI
RGB_SAI = KC.RGB_SAI
RGB_VAI = KC.RGB_VAI
WINSFTS = G(KC.LSFT(KC.S))
PANIC = KC.LCTL(KC.LALT(KC.DEL))

keyboard.keymap = [
    # layout( # QWERTY
    #     KC.Q, KC.W, KC.E, KC.R, KC.T, KC.Y, KC.U, KC.I, KC.O, KC.P,
    #     KC.TAB, KC.A, KC.S, KC.D, KC.F, KC.G, KC.LWIN, KC.ESC, KC.H, KC.J, KC.K, KC.L, JP.SCLN, JP.COLN,
    #     KC.LSFT, KC.Z, KC.X, KC.C, KC.V, KC.B, KC.RGB_TOG, KC.MB_MMB, KC.N, KC.M, JP.COMM, JP.DOT, KC.MINS, JP.SLSH,
    #     KC.LCTL, LOWER, KC.SPC, KC.ENT, RAISE, KC.RSFT,
    #     ..., KC.BSPC
    # ),
    layout( # Eucalyn
                 KC.Q,    KC.W,    JP.COMM, JP.DOT,  JP.SCLN,                   KC.M,    KC.R,    KC.D,    KC.Y,    KC.P,
        KC.TAB,  KC.A,    KC.O,    KC.E,    KC.I,    KC.U,    KC.LWIN, KC.ESC,  KC.G,    KC.T,    KC.K,    KC.S,    KC.N,    JP.COLN,
        KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,    KC.F,    RGB_TOG, MB_BTN3, KC.B,    KC.H,    KC.J,    KC.L,    KC.MINS, JP.SLSH,
                                   KC.LCTL, L_MHEN,  KC.SPC,                    KC.ENT,  R_HENK,  KC.RSFT,
                                            ALT_ESC,                                     KC.BSPC
    ),
    layout( # Raise
                 JP.EXLM, JP.DQUO, JP.HASH, JP.DLR,  JP.PERC,                   JP.AMPR, JP.QUOT, JP.LPRN, JP.RPRN, JP.GRV,
        _______, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   _______, _______, KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   JP.TILD,
        _______, JP.PIPE, JP.CIRC, JP.AT,   JP.LBRC, JP.LCBR, _______, _______, JP.RCBR, JP.RBRC, JP.UNDS, JP.DOT,  JP.BSLS, JP.QUES,
                                   _______, ADJUST,  _______,                   _______, _______, _______,
                                            _______,                                     _______
    ),
    layout( # Lower
                 KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,                     XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
        _______, KC.F6,   KC.F7,   KC.F8,   KC.F9,   KC.F10,  _______, _______, MB_BTN1, MB_BTN2, KC.UP,   XXXXXXX, XXXXXXX, XXXXXXX,
        _______, KC.F11,  KC.F12,  XXXXXXX, KC.ESC,  XXXXXXX, _______, _______, XXXXXXX, KC.LEFT, KC.DOWN, KC.RGHT, XXXXXXX, XXXXXXX,
                                   _______, _______, _______,                   _______, ADJUST,  _______,
                                            _______,                                     KC.DEL
    ),
    layout( # Adjust
                 XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                   KC.INS,  G(KC.R), G(KC.D), JP.ZKHK, KC.KANA,
        G(KC.TAB),G(KC.A),XXXXXXX, G(KC.E), XXXXXXX, XXXXXXX, _______, _______, JP.CAPS, KC.PSCR, XXXXXXX, WINSFTS, XXXXXXX, KC.RESET,
        _______, KC.LWIN, G(KC.X), XXXXXXX, G(KC.V), XXXXXXX, _______, _______, RGB_HUI, RGB_SAI, RGB_VAI, XXXXXXX, XXXXXXX, PANIC,
                                   _______, _______, _______,                   _______, _______, _______,
                                            _______,                                     _______
    ),
]

# encoder_handler.map = [
#     # [   # Qwerty
#     #     (KC.UP, KC.DOWN), (KC.MW_DN, KC.MW_UP)
#     # ],
#     [   # Eucalyn
#         # (KC.UP, KC.DOWN), (KC.MW_DN, KC.MW_UP)
#         (KC.UP, KC.DOWN), (_______, _______)
#     ],
#     [   # Raise
#         (KC.LEFT, KC.RGHT), (_______, _______)
#     ],
#     [   # Lower
#         (_______, _______), (KC.PGDN, KC.PGUP)
#     ],
#     [   # Adjust
#         (_______, _______), (_______, _______)
#     ]
# ]

if __name__ == '__main__':
    keyboard.go()
