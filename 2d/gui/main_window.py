from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QPushButton,
    QColorDialog, QHBoxLayout, QLabel
)
from core.state import AppState
from core.draw import GLCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Grafika 2D Interaktif")
        self.setGeometry(100, 100, 1000, 700)

        # ---- shared state & canvas ----
        self.state = AppState()
        self.canvas = GLCanvas(self.state)

        # ---- color picker ----
        color_btn = QPushButton("Pilih Warna")
        color_btn.clicked.connect(self._pick_color)

        # ---- draw-mode buttons ----
        mode_layout = QHBoxLayout()
        for text, mode in [
            ("Titik", "point"),
            ("Garis", "line"),
            ("Persegi", "square"),
            ("Ellipse", "ellipse"),
        ]:
            btn = QPushButton(text)
            btn.clicked.connect(lambda _chk, m=mode: self.state.set_mode(m))
            mode_layout.addWidget(btn)

        # ---- thickness control ----
        from PyQt5.QtWidgets import QSlider
        from PyQt5.QtCore import Qt

        thickness_layout = QHBoxLayout()
        thickness_label = QLabel("Ketebalan: 2")
        thickness_slider = QSlider(Qt.Horizontal)
        thickness_slider.setMinimum(1)
        thickness_slider.setMaximum(10)
        thickness_slider.setValue(2)
        thickness_slider.setTickPosition(QSlider.TicksBelow)
        thickness_slider.setTickInterval(1)
        thickness_slider.valueChanged.connect(lambda val: self._set_thickness_slider(val, thickness_label))

        thickness_layout.addWidget(QLabel("Ketebalan Garis"))
        thickness_layout.addWidget(thickness_slider)
        thickness_layout.addWidget(thickness_label)

        # ---- clear canvas ----
        clear_btn = QPushButton("Clear Canvas")
        clear_btn.clicked.connect(self._clear_canvas)

        # ---- on-screen hint ----
        hint = QLabel("""
Shortcut:
• ← ↑ ↓ →  →  Translasi (geser)
• R / T       →  Rotasi
• + / -       →  Perbesar / Perkecil
""")
        hint.setStyleSheet("color:#666;font-size:11px; line-height:1.4em")

        # ---- assemble layout ----
        wrap = QWidget()
        main_layout = QHBoxLayout(wrap)

        # Left: canvas (besar)
        main_layout.addWidget(self.canvas, stretch=3)

        # Right: panel kontrol (samping)
        control_panel = QVBoxLayout()
        control_panel.addLayout(mode_layout)
        control_panel.addWidget(color_btn)
        control_panel.addLayout(thickness_layout)
        control_panel.addWidget(clear_btn)
        control_panel.addWidget(hint)
        control_panel.addStretch()

        main_layout.addLayout(control_panel, stretch=1)
        self.setCentralWidget(wrap)

    # ---------- helpers ----------
    def _set_thickness_slider(self, val, label):
        label.setText(f"Ketebalan: {val}")
        self.state.set_thickness(val)
        self.canvas.update()

    def _set_thickness(self, val):
        self.state.set_thickness(val)
        self.canvas.update()

    def _clear_canvas(self):
        self.state.objects.clear()
        self.canvas.update()

    def _pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.state.set_color(color.redF(), color.greenF(), color.blueF())
            self.canvas.update()
