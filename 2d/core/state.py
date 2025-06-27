class AppState:
    """Holds global drawing state shared between UI and GL canvas."""

    def __init__(self):
        self.objects = []              # drawn objects
        self.current_color = (1.0, 1.0, 1.0)
        self.line_width = 2            # default thickness
        self.current_mode = "point"    # drawing tool
        self.window_bounds = None      # for future clipping

    # ---- setters ----
    def set_color(self, r: float, g: float, b: float):
        self.current_color = (r, g, b)

    def set_mode(self, mode: str):
        self.current_mode = mode

    def set_thickness(self, w: int):
        """Update default line width for new objects."""
        self.line_width = max(1, min(10, int(w)))
