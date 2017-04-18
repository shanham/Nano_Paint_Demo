""" NanoPaint.py 

Science festival demonstration showing how nanoscale structure leads to colouration

Author: Dr Stephen Hanham

"""

import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Main_Window import Ui_MainWindow
from SVGPaintView import SVGPaintView
from PyQt4 import QtOpenGL
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from guiqwt.builder import make
from guiqwt.curve import CurvePlot
import numpy as np
import scipy
import scipy.interpolate as si

class NanoPaint(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None, app_ref=None):
        super(NanoPaint, self).__init__(parent)
        self.setupUi(self)
        self.showFullScreen()

        #glformat = QtOpenGL.QGLFormat()
        #glformat.setVersion(3, 3)
        #glformat.setProfile(QtOpenGL.QGLFormat.CoreProfile)

        self.cyl_diameter = self.diameter_slider.value()
        self.cyl_period = self.period_slider.value()
        self.diameter_slider.valueChanged.connect(self.update_diameter)
        self.period_slider.valueChanged.connect(self.update_period)

        # Load butterfly SVG once window is resized to full screen
        self.graphics_view_widget.setup("butterfly9.svg", "butterfly_areas.dat")

        self.setup_refl_graph()
        self.load_refl_data()
        self.update_refl_graph()

    def update_diameter(self):
        """ Updates the cylinder diameter """
        self.diameter_value_label.setText(str(self.diameter_slider.value()) + " (nm)")
        self.cyl_diameter = self.diameter_slider.value()
        self.update_cyl()
        self.update_refl_graph()
        self.calc_current_colour()

    def update_period(self):
        self.period_value_label.setText(str(self.period_slider.value()) + " (nm)")
        self.cyl_period = self.period_slider.value()
        self.update_cyl()
        self.update_refl_graph()

    def update_cyl(self):
        self.cyl_view_widget.update_geom(self.cyl_diameter, self.cyl_period)

    def setup_refl_graph(self):
        self.lam = np.linspace(450, 750, 100)
        self.plot_curve = make.curve(1,1, color='b')
        self.plot = self.refl_graph.get_plot()
        self.plot.add_item(self.plot_curve)
        self.plot.set_titles(xlabel='Wavelength (nm)', ylabel='Reflectance')
        label_font = QFont("Arial", 10)
        label_font.setBold(True)
        self.plot.set_axis_font("left", label_font)
        self.plot.set_axis_font("bottom", label_font)
        self.plot.setAxisMaxMajor(self.plot.get_axis_id('left'), 5)
        self.plot.setAxisMaxMinor(self.plot.get_axis_id('left'), 5)
        axis_id = self.plot.get_axis_id('left')
        self.plot.set_axis_limits(axis_id, 0, 1)
        self.refl_graph.show()

    def update_refl_graph(self):
        ''' Update reflection graph with current slider values '''
        self.curr_refl = self.calc_refl(self.diameter_slider.value(), self.period_slider.value(), self.lam)
        self.plot_curve.set_data(self.lam, self.curr_refl)
        r,g,b = self.calc_current_colour()
        self.plot_curve.setPen(QColor(int(r*255),int(g*255),int(b*255)))
        self.graphics_view_widget.paint_colour = self.calc_current_colour()

    def load_refl_data(self):
        # Load data from CSV
        # But for now lets use random data
        diam = np.linspace(300,450,20)
        period = np.linspace(600, 1400, 20)
        wavelength = np.linspace(450, 750, 100)
        self.points_data = (diam, period, wavelength)  # Points tuple
        self.refl_data = np.random.rand(20,20,100)

    def calc_refl(self, diam, period, wavelength):
        ''' Returns the reflectance for a given diameter/period.
            NB. Assumes len(diam) = len(period) = 1 and len(wavelength) = n
        '''
        n = np.size(wavelength)
        xi = (diam*np.ones(n),period*np.ones(n),wavelength)
        yi = si.interpn(self.points_data, self.refl_data, xi, method='linear', bounds_error=True)
        return yi

    def calc_current_colour(self):
        ''' Returns a colour value by integrating reflectance curve over corresponding wavelength regions '''
        ri = np.logical_and(self.lam >= 620, self.lam <= 750)
        gi = np.logical_and(self.lam >= 495, self.lam <= 570)
        bi = np.logical_and(self.lam >= 450, self.lam <= 495)

        red_val = np.sum(self.curr_refl[ri])/np.size(self.curr_refl[ri])
        green_val = np.sum(self.curr_refl[gi]) / np.size(self.curr_refl[gi])
        blue_val = np.sum(self.curr_refl[bi]) / np.size(self.curr_refl[bi])

        return (red_val,green_val,blue_val)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = NanoPaint(app_ref=app)
    ret = app.exec_()
    sys.exit(ret)
