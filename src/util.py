# code to handle string formatting when printing to terminal
# we'll use this later on

class colors:

    RESET  = '\x1b[49;0m'
    DARK   = '\x1b[38;5;232;1m'
    LIGHT  = '\x1b[38;5;231;1m'
    WHITE  = '\x1b[38;5;231;0m'
    GREEN  = '\x1b[38;5;2;1m'
    YELLOW = '\x1b[38;5;226;1m'
    ORANGE = '\x1b[38;5;208;1m'
    RED    = '\x1b[38;5;1m'
    GRAY   = '\x1b[38;5;242m'
    BOLD   = '\x1b[1m'
    UNDERLINE  = '\x1b[4m'
    BLINKING = '\33[5m'
    DULL_GRAY  = '\x1b[38;5;238;1m'
    DULL_GREEN = '\x1b[38;5;28;1m'

class backgrounds:

    GREEN_DARK  = '\x1b[48;5;136;1m'
    GREEN_LIGHT = '\x1b[48;5;143;1m'
    PURPLE_DARK  = '\x1b[48;5;176;1m'
    PURPLE_LIGHT = '\x1b[48;5;177;1m'
    DARK  = '\x1b[48;5;172;1m'
    LIGHT = '\x1b[48;5;215;1m'
    BLACK = '\x1b[48;5;232;1m'
    WHITE = '\x1b[48;5;15;1m'
    RED   = '\x1b[48;5;9;1m'

class paddings:

    CENTER_PAD = "\t        "
    MIN_PAD = "       "
    MID_PAD = "\t\t          "
    BIG_PAD = "\t\t            "

