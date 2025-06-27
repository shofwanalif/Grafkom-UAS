from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtCore import Qt
from OpenGL.GL import *  # noqa
from OpenGL.GLU import *  # noqa
import math
from math import cos, sin, pi

PREVIEW_SEGMENTS = 100
STEP_TRANSLATE = 5
STEP_ROTATE = 5
STEP_SCALE = 0.05

class GLCanvas(QGLWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self._dragging = False
        self._start = self._end = None

    # ---- lifecycle ----
    def initializeGL(self):
        glClearColor(1,1,1,1)
        glEnable(GL_POINT_SMOOTH)
        glPointSize(5)

    def resizeGL(self, w, h):
        glViewport(0,0,w,h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, w, h, 0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        for obj in self.state.objects:
            glColor3f(*obj['color'])
            glLineWidth(obj.get('width', self.state.line_width))
            glBegin(obj['type'])
            for vx, vy in obj['vertices']:
                glVertex2f(vx, vy)
            glEnd()
        if self._dragging and self._start and self._end:
            glColor3f(*self.state.current_color)
            glLineWidth(1)
            self._draw_preview()

    # ---- mouse ----
    def mousePressEvent(self, e):
        if e.button()!=Qt.LeftButton: return
        x,y = e.x(), e.y()
        mode = self.state.current_mode
        if mode=='point':
            self.state.objects.append({
                'type': GL_POINTS,
                'vertices': [(x,y)],
                'color': self.state.current_color,
                'width': self.state.line_width
            })
            self.update()
        else:
            self._dragging=True; self._start=(x,y); self._end=(x,y)
            self.update()

    def mouseMoveEvent(self, e):
        if self._dragging:
            self._end=(e.x(), e.y())
            self.update()

    def mouseReleaseEvent(self, e):
        if self._dragging and e.button()==Qt.LeftButton:
            self._end=(e.x(), e.y())
            self._commit_shape()
            self._dragging=False; self._start=self._end=None
            self.update()

    # ---- keyboard ----
    def keyPressEvent(self, e):
        if not self.state.objects: return
        k=e.key()
        if k==Qt.Key_Left:
            self._translate(-STEP_TRANSLATE,0)
        elif k==Qt.Key_Right:
            self._translate(STEP_TRANSLATE,0)
        elif k==Qt.Key_Up:
            self._translate(0,-STEP_TRANSLATE)
        elif k==Qt.Key_Down:
            self._translate(0,STEP_TRANSLATE)
        elif k==Qt.Key_R:
            self._rotate(-STEP_ROTATE)
        elif k==Qt.Key_T:
            self._rotate(STEP_ROTATE)
        elif k in (Qt.Key_Plus, Qt.Key_Equal):
            self._scale(1+STEP_SCALE)
        elif k in (Qt.Key_Minus, Qt.Key_Underscore):
            self._scale(1-STEP_SCALE)
        self.update()

    # ---- transforms ----
    def _translate(self, dx, dy):
        from core.transform import apply_transform
        apply_transform(self.state.objects[-1], [1,0,0,1,dx,dy])

    ...
    def _rotate(self, deg):
        from core.transform import apply_transform
        a = math.radians(deg)
        mat = [math.cos(a), math.sin(a), -math.sin(a), math.cos(a), 0, 0]
        obj = self.state.objects[-1]
        cx, cy = self._centroid(obj['vertices'])
        apply_transform(obj, mat, pivot=(cx, cy))

    def _scale(self, factor):
        from core.transform import apply_transform
        mat = [factor, 0, 0, factor, 0, 0]
        obj = self.state.objects[-1]
        cx, cy = self._centroid(obj['vertices'])
        apply_transform(obj, mat, pivot=(cx, cy))

    def _centroid(self, vertices):
        sx = sum(x for x, _ in vertices)
        sy = sum(y for _, y in vertices)
        n = len(vertices)
        return sx / n, sy / n

    # ---- preview & commit ----
    def _draw_preview(self):
        mode = self.state.current_mode
        x0, y0 = self._start
        x1, y1 = self._end
        if mode == 'line':
            glBegin(GL_LINES)
            glVertex2f(x0, y0)
            glVertex2f(x1, y1)
            glEnd()
        elif mode == 'square':
            glBegin(GL_LINE_LOOP)
            glVertex2f(x0, y0)
            glVertex2f(x1, y0)
            glVertex2f(x1, y1)
            glVertex2f(x0, y1)
            glEnd()
        elif mode == 'ellipse':
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            rx, ry = abs(x1 - x0) / 2, abs(y1 - y0) / 2
            glBegin(GL_LINE_LOOP)
            for i in range(PREVIEW_SEGMENTS):
                theta = 2 * pi * i / PREVIEW_SEGMENTS
                glVertex2f(cx + rx * cos(theta), cy + ry * sin(theta))
            glEnd()

    def _commit_shape(self):
        mode = self.state.current_mode
        x0, y0 = self._start
        x1, y1 = self._end
        col = self.state.current_color
        width = self.state.line_width
        if mode == 'line':
            obj = {'type': GL_LINES, 'vertices': [(x0, y0), (x1, y1)], 'color': col, 'width': width}
        elif mode == 'square':
            obj = {'type': GL_LINE_LOOP, 'vertices': [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], 'color': col, 'width': width}
        elif mode == 'ellipse':
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            rx, ry = abs(x1 - x0) / 2, abs(y1 - y0) / 2
            verts = [(cx + rx * cos(2 * pi * i / PREVIEW_SEGMENTS), cy + ry * sin(2 * pi * i / PREVIEW_SEGMENTS)) for i in range(PREVIEW_SEGMENTS)]
            obj = {'type': GL_LINE_LOOP, 'vertices': verts, 'color': col, 'width': width}
        else:
            return
        self.state.objects.append(obj)

