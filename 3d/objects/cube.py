from OpenGL.GL import *

# 8 titik sudut kubus (x, y, z)
vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
]

# Setiap face berisi 4 index ke array vertices
faces = [
    [0, 1, 2, 3],  # Belakang
    [4, 5, 6, 7],  # Depan
    [0, 1, 5, 4],  # Bawah
    [2, 3, 7, 6],  # Atas
    [1, 2, 6, 5],  # Kanan
    [0, 3, 7, 4]   # Kiri
]

colors = [
    [1, 0, 0],  # Merah
    [0, 1, 0],  # Hijau
    [0, 0, 1],  # Biru
    [1, 1, 0],  # Kuning
    [1, 0, 1],  # Magenta
    [0, 1, 1]   # Cyan
]

def draw_cube():
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glColor3fv(colors[i])
        for vert in face:
            glVertex3fv(vertices[vert])
    glEnd()
