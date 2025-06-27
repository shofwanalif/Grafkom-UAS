from OpenGL.GL import *
from PyQt5.QtCore import Qt

class Transform3D:
    """Menyimpan dan menerapkan transformasi translasi & rotasi untuk objek 3D."""
    def __init__(self):
        # Translasi
        self.tx = 0.0
        self.ty = 0.0
        self.tz = 0.0
        # Rotasi (derajat)
        self.rx = 0.0
        self.ry = 0.0

    # ------------------------------------------------------------------
    # Metode untuk menerapkan transformasi pada matriks MODELVIEW aktif
    # ------------------------------------------------------------------
    def apply(self):
        """Apply translation and rotation to the current MODELVIEW matrix."""
        glTranslatef(self.tx, self.ty, self.tz)
        glRotatef(self.rx, 1.0, 0.0, 0.0)  # Rotasi sumbu X
        glRotatef(self.ry, 0.0, 1.0, 0.0)  # Rotasi sumbu Y

    # ------------------------------------------------------------------
    # Input handling helpers
    # ------------------------------------------------------------------
    def handle_key(self, key):
        """Update translation/rotation based on pressed key."""
        step_t = 0.1     # step translasi
        step_r = 5.0     # step rotasi

        if key == Qt.Key_W:
            self.ty += step_t
        elif key == Qt.Key_S:
            self.ty -= step_t
        elif key == Qt.Key_A:
            self.tx -= step_t
        elif key == Qt.Key_D:
            self.tx += step_t
        elif key == Qt.Key_Q:
            self.tz += step_t
        elif key == Qt.Key_E:
            self.tz -= step_t
        elif key == Qt.Key_Left:
            self.ry -= step_r
        elif key == Qt.Key_Right:
            self.ry += step_r
        elif key == Qt.Key_Up:
            self.rx -= step_r
        elif key == Qt.Key_Down:
            self.rx += step_r
