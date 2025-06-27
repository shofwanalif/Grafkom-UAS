from OpenGL.GL import *

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Ambient light
    ambient = [0.2, 0.2, 0.2, 1.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)

    # Diffuse light
    diffuse = [0.7, 0.7, 0.7, 1.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)

    # Specular light
    specular = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)

    # Posisi sumber cahaya
    position = [5.0, 5.0, 5.0, 1.0]  # Posisi point light
    glLightfv(GL_LIGHT0, GL_POSITION, position)

    # Material object
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
    glMateriali(GL_FRONT_AND_BACK, GL_SHININESS, 50)
