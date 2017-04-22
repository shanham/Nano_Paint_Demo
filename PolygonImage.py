import pickle
#from PyQt4 import QtCore

class PolygonImage:

    def __init__(self):
        self.polygons_list = []  # Holds a list of QPolygons
        self.id_list = []  # Holds a list of string ids
        self.diam_list = []  # Holds the painted cylinder diameters
        self.period_list = []  # Holds the painted cylinder's period

    def add_polygon(self, polygon, id):
        self.polygons_list.append(polygon)
        self.id_list.append(id)
        self.diam_list.append(0)
        self.period_list.append(0)

    def check_point(self, point):
        """ Returns ID of polygon containing point, otherwise returns empty string """
        for i, poly in enumerate(self.polygons_list):
            if poly.containsPoint(point, 0):
                return self.id_list[i], self.diam_list[i], self.period_list[i], i
        return "", -1, -1, -1

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)


