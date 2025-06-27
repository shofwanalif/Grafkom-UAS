INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8

def compute_outcode(x, y, xmin, ymin, xmax, ymax):
    code = INSIDE
    if x < xmin: code |= LEFT
    elif x > xmax: code |= RIGHT
    if y < ymin: code |= BOTTOM
    elif y > ymax: code |= TOP
    return code

def clip_line(x0, y0, x1, y1, bounds):
    xmin, ymin, xmax, ymax = bounds
    out0 = compute_outcode(x0, y0, xmin, ymin, xmax, ymax)
    out1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
    while True:
        if not (out0 | out1):
            return x0, y0, x1, y1  # trivially inside
        if out0 & out1:
            return None           # trivially outside
        out = out0 or out1
        if out & TOP:
            x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0); y = ymax
        elif out & BOTTOM:
            x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0); y = ymin
        elif out & RIGHT:
            y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0); x = xmax
        else:  # LEFT
            y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0); x = xmin
        if out == out0:
            x0, y0, out0 = x, y, compute_outcode(x, y, xmin, ymin, xmax, ymax)
        else:
            x1, y1, out1 = x, y, compute_outcode(x, y, xmin, ymin, xmax, ymax)
