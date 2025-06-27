import math

def apply_transform(obj: dict, m, pivot=None):
    a, b, c, d, e, f = m  # 2×3 matrix flattened
    if pivot is None:
        px = py = 0
    else:
        px, py = pivot
    new = []
    for x, y in obj['vertices']:
        x -= px; y -= py
        nx = a * x + c * y + e
        ny = b * x + d * y + f
        new.append((nx + px, ny + py))
    obj['vertices'] = new
    return obj