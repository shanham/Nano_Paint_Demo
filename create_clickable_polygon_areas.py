# Script to create polygon representation of SVG file path objects to speedup click detection
# This script should be run before running the main code.
# The SVG file should be specially prepared in Inkscape by setting the ID to areaX where X is a number

from lxml import etree
import numpy as np
import matplotlib.pyplot as plt
from svgpathtools import *
from PyQt4 import QtGui, QtCore
from PolygonImage import PolygonImage

# Parse SVG file and pullout path tags
tree = etree.parse("butterfly9.svg")

poly_image = PolygonImage()
points = []

#Iterate through designated paths with ID starting with "area"
for elem in tree.iter():
    if elem.tag == '{http://www.w3.org/2000/svg}path' and elem.attrib['id'][0:4] == "area":
        path = parse_path(elem.attrib['d'])

        # Just take the first path for two particular areas
        if elem.attrib['id'] == "area12" or elem.attrib['id'] == "area13":
            path = path.continuous_subpaths()[0]

        # Sample 1000 points on path
        poly = QtGui.QPolygon(1000)
        k = 0
        for i in np.linspace(0,1,1000):
            scale = 10
            p = path.point(i)*scale
            points.append(p)

            poly.setPoint(k, np.real(p), np.imag(p))
            k += 1

        # Create polygon from points
        poly_image.add_polygon(poly, elem.attrib['id'])

        plt.plot(np.real(points), np.imag(points))
        points = []

poly_image.save("butterfly_areas.dat")
plt.show()

