from PyQt5 import QtWidgets
from .box_model import BoxModel
from .compartment import CompartmentSystem
from .cutout import CutoutPattern
from .splitter import AutoSplitter

class MainWindow(QtWidgets.QMainWindow):
    """Main application window with basic box editor."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("STL Box Designer")
        self.box_model = BoxModel()
        self.compartment_system = CompartmentSystem(self.box_model)
        self.cutout_pattern = CutoutPattern(self.box_model)
        self.splitter = AutoSplitter(self.box_model)
        self._build_ui()

    def _build_ui(self):
        central = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout(central)

        self.x_input = QtWidgets.QSpinBox()
        self.x_input.setRange(1, 1000)
        self.x_input.setValue(100)
        self.y_input = QtWidgets.QSpinBox()
        self.y_input.setRange(1, 1000)
        self.y_input.setValue(100)
        self.z_input = QtWidgets.QSpinBox()
        self.z_input.setRange(1, 1000)
        self.z_input.setValue(50)

        layout.addRow("Length (X)", self.x_input)
        layout.addRow("Width (Y)", self.y_input)
        layout.addRow("Height (Z)", self.z_input)

        apply_btn = QtWidgets.QPushButton("Apply")
        apply_btn.clicked.connect(self.apply_dimensions)
        layout.addRow(apply_btn)

        self.setCentralWidget(central)

    def apply_dimensions(self):
        """Apply dimension changes to the box model."""
        x = self.x_input.value()
        y = self.y_input.value()
        z = self.z_input.value()
        self.box_model.set_dimensions(x, y, z)
        # further UI updates or previews would go here


def launch():
    app = QtWidgets.QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()

if __name__ == "__main__":
    launch()
