from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtSvg import *
from PyQt4.QtXml import *
from PolygonImage import PolygonImage
import numpy as np

class SVGPaintView(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.paint_colour = (0, 0, 1)  # Current colour to paint with (red,green,blue)

    def setup(self, svg_file, svg_areas_file):
        # Load polygon image which defines clickable regions
        try:
            self.poly_image = PolygonImage.load(svg_areas_file)
        except:
            print("Could not load butterfly regions file")
            raise RuntimeError()

        # Load SVG file for display
        f = QFile(svg_file)
        if not f.open(QIODevice.ReadOnly):
            print("Failed to open file")
            raise RuntimeError()

        self.svg_doc = QDomDocument()  # Variable containing SVG data
        if not self.svg_doc.setContent(f):
            f.close()
            print("SVG XML contents not set")
            raise RuntimeError()

        self.doc = QSvgRenderer(self.svg_doc.toByteArray(), self)
        self.connect(self.doc, SIGNAL("repaintNeeded()"), self, SLOT("update()"))

        #self.resize(300, 200)
        self.scale_x = self.doc.viewBox().width() / self.width()  # Scaling for SVG file in x
        self.scale_y = self.doc.viewBox().height() / self.height()  # Scaling for SVG file in y

        #self.setCursor(QtGui.QCursor(QtGui.QPixmap("bucket.ico")))
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setViewport(0, 0, self.width(), self.height())
        self.doc.render(p)

    # def sizeHint(self):
    #     if self.doc:
    #         return self.doc.defaultSize()
    #     return QWidget.sizeHint(self)

    def mousePressEvent(self, event):
        mouse_press_pos = QPoint(event.pos())
        svg_point = QPoint(mouse_press_pos.x() * self.scale_x, mouse_press_pos.y() * self.scale_y)
        id_clicked = self.poly_image.check_point(svg_point)
        if id_clicked != "":
            print("Clicked on ID " + id_clicked)
            col_str = "#%02x%02x%02x" % tuple(np.array(self.paint_colour)*255)
            print("Colour is " + col_str)
            self.change_svg_region_colour(id_clicked, col_str)
        event.accept()

    def change_svg_region_colour(self, id, colour):
        """ Changes the colour of a path with supplied id in the svg file in memory and updates the widget """
        root = self.svg_doc.documentElement()
        curr_node = root.firstChild()

        # Search for correct SVG path to change
        while not curr_node.isNull():
            elem = curr_node.toElement()

            if elem.tagName() == "path" and elem.attribute('id') == id:
                print("Changing colour of element " + elem.attribute('id'))
                style = elem.attribute("style")
                style = style[0:5] + colour + style[12:]
                elem.setAttribute("style", style)

            curr_node = curr_node.nextSibling()

        self.doc = QSvgRenderer(self.svg_doc.toByteArray(), self)  # Update renderer data
        self.repaint()