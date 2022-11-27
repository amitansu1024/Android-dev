import os
import sys
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeCone, BRepPrimAPI_MakeTorus
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Common, BRepAlgoAPI_Fuse

from PyQt5.QtWidgets import (QMenu, QMainWindow, QVBoxLayout, QGroupBox, QApplication)

from OCC.Display.backend import load_backend
load_backend("qt-pyqt5")
import OCC.Display.qtDisplay as qtDisplay

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "PyCad"
        self.left = 300
        self.top = 300
        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.top, 300, 300)
        self.createViewer()

        self.setCentralWidget(self.viewer)
        self.createMenu()
        self.display.SetSelectionModeShape()
        self.display.register_select_callback(self.select_shape)
        self.shapes = self.display.selected_shapes
        self.show()


    def createViewer(self):
        self.viewer = QGroupBox()
        layout = QVBoxLayout()

        self.canvas = qtDisplay.qtViewer3d(self)
        layout.addWidget(self.canvas)
        self.canvas.resize(200, 200)
        self.canvas.InitDriver()
        self.display = self.canvas._display

        self.viewer.setLayout(layout)


    def createMenu(self):
        self.menubar = self.menuBar()
        self.setMenuBar(self.menubar)
        self.menu_file = QMenu()
        self.menu_operation = QMenu()
        self.menu_Erase = QMenu()

        self.menu_file = self.menubar.addMenu("Draw")
        self.fileBox = self.menu_file.addAction("Cube", self.box, 0)
        self.fileSphere = self.menu_file.addAction("Sphere", self.sphere, 0)
        self.fileCone = self.menu_file.addAction("Cone", self.cone, 0)
        self.fileTorus = self.menu_file.addAction("Torus", self.torus, 0)

        self.menu_operation = self.menubar.addMenu("Operations")
        self.operationsCut = self.menu_operation.addAction("Cut", self.boolean_cut, 0)
        self.operationsCommon = self.menu_operation.addAction("Common", self.boolean_common, 0)
        self.operationsFuse = self.menu_operation.addAction("Fuse", self.boolean_fuse, 0)

        self.menu_erase = self.menubar.addMenu("Erase")
        self.erase_all = self.menu_erase.addAction("Erase all", self.eraseAll, 0)

    def eraseAll(self):
        self.display.EraseAll()

    def box(self):
        box = BRepPrimAPI_MakeBox(10, 10, 10).Shape()
        self.shapes.append(box)
        self.display.DisplayColoredShape(box, "YELLOW", True)

    def sphere(self):
        sphere = BRepPrimAPI_MakeSphere(15).Shape()
        self.shapes.append(sphere)
        self.display.DisplayColoredShape(sphere, "RED", True)

    def cone(self):
        cone = BRepPrimAPI_MakeCone(0, 10, 20).Shape()
        self.shapes.append(cone)
        self.display.DisplayColoredShape(cone, "BLUE", True)

    def torus(self):
        torus = BRepPrimAPI_MakeTorus(5, 10).Shape()
        self.shapes.append(torus)
        self.display.DisplayColoredShape(torus, "GREEN", True)

    def boolean_cut(self):
        Cut = BRepAlgoAPI_Cut(self.shapes[0], self.shapes[1]).Shape()
        self.display.EraseAll()
        self.display.DisplayShape(Cut)
        self.display.FitAll()

    def boolean_common(self):
        common = BRepAlgoAPI_Common(self.shapes[0], self.shapes[1]).Shape()
        self.display.EraseAll()
        self.display.DisplayShape(common)
        self.display.FitAll()

    def boolean_fuse(self):
        fuse = BRepAlgoAPI_Fuse(self.shapes[0], self.shapes[1]).Shape()
        self.display.EraseAll()
        self.display.DisplayShape(fuse)
        self.display.FitAll()

    def second_select(self, shp, *kwargs):
        for shape in shp:
            self.shapes.append(shape)
            print("More Shape selected: ", shape)

    def select_shape(self, shp, *kwargs):
        self.shapes = []
        for shape in shp:
            self.shapes.append(shape)
            print("Shape selected: ", shape)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    if os.getenv("APPVEYOR") is None:
        sys.exit(app.exec_())
