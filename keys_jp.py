from kmk.keys import KC

_S = lambda key: KC.LSFT(key)

ZKHK = KC.ZKHK                      # JIS Zenkaku/Hankaku
MINUS = MINS = KC.MINS              # -
CIRCUMFLEX = CIRC = KC.EQL          # ^
YEN = KC.JYEN                       # ¥ 
AT = KC.LBRC                        # @
LBRACKET = LBRC = KC.RBRC           # [
SCOLON = SCLN = KC.SCLN             # ;
COLON = COLN = KC.QUOT              # :
RBRACKET = RBRC = KC.NUHS           # ]
COMMA = COMM = KC.COMM              # , and <
DOT = KC.DOT                        # . and >
SLASH = SLSH = KC.SLSH              # /
BSLASH = BSLS = KC.INT1             # \ 

EXCLAIM = EXLM = _S(KC.N1)              # !
DOUBLE_QUOTE = DQUO = DQT = _S(KC.N2)   # "
HASH = _S(KC.N3)                        # #
DOLLAR = DLR = _S(KC.N4)                # $
PERCENT = PERC = _S(KC.N5)              # %
AMPERSAND = AMPR = _S(KC.N6)            # &
QUOTE = QUOT = _S(KC.N7)                # '
LEFT_PAREN = LPRN = _S(KC.N8)           # (
RIGHT_PAREN = RPRN = _S(KC.N9)          # )
EQUAL = EQL = _S(MINS)                  # =
TILDE = TILD = _S(CIRC)                 # ~
PIPE = _S(KC.JYEN)                      # |
GRAVE = GRV = _S(AT)                    # `
LEFT_CURLY_BRACE = LCBR = _S(LBRC)      # {
CAPSLOCK = CLCK = CAPS = _S(KC.CAPS)    # Caps Lock
PLUS = _S(SCLN)                         # +
ASTERISK = ASTR = _S(COLN)              # *
RIGHT_CURLY_BRACE = RCBR = _S(RBRC)     # }
LEFT_ANGLE_BRACKET = LABK = LT = _S(COMM) # <
RIGHT_ANGLE_BRACKET = RABK = GT = _S(DOT) # >
QUESTION = QUES = _S(SLSH)              # ?
UNDERSCORE = UNDS = _S(BSLS)            # _
