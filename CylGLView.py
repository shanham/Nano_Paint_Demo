""" Qt Widget for displaying a cylinder array using OpenGL 

    Author: Dr Stephen Hanham
"""

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt4 import QtGui, QtOpenGL

class CylGLView(QtOpenGL.QGLWidget):

    def initializeGL(self):
        glViewport(0, 0, self.width(), self.height())

        quadratic = gluNewQuadric()
        gluQuadricDrawStyle(quadratic, GLU_FILL)
        gluQuadricNormals(quadratic, GLU_SMOOTH)  # Create Smooth Normals (NEW)

        glClearColor(0.95, 0.95, 0.95, 1.)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        lightZeroPosition = [0, 15., 15, 1.]
        lightZeroColor = [1, 1.0, 1, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.01)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.02)
        glEnable(GL_LIGHT0)
        #glutDisplayFunc(self.paintGL)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(40., 1., 0.1, 4000.)
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(0, 40, 50,  # Camera pos (x,y,z)
                  0, 20, 25,  # Camera pointed towards (x,y,z)
                  0, -1, 0)  # Camera orientation (x,y,z)
        glPushMatrix()

        self.diameter = 5
        self.period = 10

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cyl_colour = [1.0, 0., 0., 1.]
        box_colour = [0, 0, 0, 1]

        m = 5
        x_list = np.linspace(-m*self.period, m*self.period, 2*m + 1)
        y_list = np.linspace(-m*self.period, m*self.period, 2*m + 1)

        # Draw cylinder array
        for i in range(len(x_list)-1):
            for k in range(len(y_list)-1):
                x = x_list[i]
                y = y_list[k]
                self.draw_cylinder(x, y, 0, self.diameter / 2.0, 10, cyl_colour)

        self.draw_box(0.0, 0, 6, self.period, self.period, 12, box_colour)


    def draw_box(self, x, y, z, dx, dy, dz, colour):
        ''' Draws a rectangular box centred at (x,y,z) with dimensions (dx,dy,dz) and supplied colour '''
        glPushMatrix()
        glDisable(GL_LIGHTING)  # Turn off lighting to render box
        glColor3f(0.0, 0, 0)
        glScalef(dx, dy, dz)  # Scale space
        glTranslatef(x/dx, y/dy, z/dz)  # Re-centre at (x,y,z)
        glutWireCube(1)
        glPopMatrix()
        glEnable(GL_LIGHTING)

    def draw_cylinder(self, x, y, z, radius, height, colour):
        ''' Draws a cylinder centred at (x,y,z) with given radius, height and colour '''
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, colour)
        glPushMatrix()
        glTranslatef(x, y, z)

        # Draw side of cylinder using quadric fn
        quadObj = gluNewQuadric()
        gluQuadricDrawStyle(quadObj, GLU_FILL)
        gluQuadricNormals(quadObj, GLU_SMOOTH)
        gluCylinder(quadObj, radius, radius, height, 24, 24)

        gluDisk(quadObj, 0, radius, 100, 24)  # Bottom disk
        glTranslatef(0, 0, height)
        gluDisk(quadObj, 0, radius, 100, 24)  # Top disk
        glPopMatrix()

    def update_geom(self, diam, period):
        ''' Updates the geometry of the cylinder and repaints '''
        self.diameter = diam/100
        self.period = period/100
        self.repaint()
