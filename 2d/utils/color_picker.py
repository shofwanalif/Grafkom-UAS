COLOR_MAP = {
    'r': (1, 0, 0),
    'g': (0, 1, 0),
    'b': (0, 0, 1),
    'w': (1, 1, 1),
    'k': (0, 0, 0),
}

def get_color_from_key(key: str):
    return COLOR_MAP.get(key, (1, 1, 1))
