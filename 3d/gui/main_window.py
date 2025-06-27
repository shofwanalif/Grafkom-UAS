import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget,  QMessageBox
from PyQt5.QtOpenGL import  QGLWidget
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *

from core.transform3d import Transform3D
from core.lighting import setup_lighting
from objects.cube import draw_cube


class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.transform = Transform3D()
        # Pastikan kanvas menerima focus keyboard
        self.setFocusPolicy(Qt.StrongFocus)

    
    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.1, 0.1, 1.0)
        setup_lighting()

    def resizeGL(self, w: int, h: int):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h if h != 0 else 1.0
        gluPerspective(45.0, aspect, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Kamera di (5,5,5) menghadap origin
        gluLookAt(5.0, 5.0, 5.0,   # eye
                  0.0, 0.0, 0.0,   # center
                  0.0, 1.0, 0.0)   # up

        # Aplikasikan transformasi kemudian gambar objek
        self.transform.apply()
        draw_cube()

    def keyPressEvent(self, event):
        
        
        self.transform.handle_key(event.key())
        self.update()

    def show_help(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Kontrol Aplikasi 3D")
        msg.setText(
            "<b>Shortcut Kontrol:</b><br><br>"
            "W / A / S / D - Translasi X & Y<br>"
            "Q / E         - Translasi Z<br>"
            "Panah ← ↑ → ↓ - Rotasi sumbu X & Y<br><br>"
            "Tekan tombol ini saat jendela aktif."
        )
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
  


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Viewer with PyOpenGL")
        self.setGeometry(100, 100, 800, 600)

        # Inisialisasi GL widget
        self.gl_widget = GLWidget(self)
        
        # Layout sederhana satu kolom
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.gl_widget)
        self.setCentralWidget(central_widget)

        # Pastikan GLWidget langsung menerima fokus saat aplikasi mulai
        self.gl_widget.setFocus()
