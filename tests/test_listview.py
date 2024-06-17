import sys
import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Plot with Navigation Example")
        self.setGeometry(100, 100, 800, 600)

        # Create a Matplotlib figure and 3D subplot
        fig = Figure()
        self.ax3d = fig.add_subplot(111, projection="3d")
        # self.ax3d.set_axis_off()

        # Points data
        points = np.array([
            [4600, 13125], [4600, 2250], [0, 2250], [0, 0], [13900, 0],
            [13900, 2250], [6600, 2250], [6600, 7625], [23300, 7625],
            [23300, 2250], [18000, 2250], [18000, 0], [29000, 0], [29000, 2250],
            [25300, 2250], [25300, 13125], [23300, 13125], [23300, 8625],
            [6600, 8625], [6600, 13125]
        ])

        # Convert to numpy arrays
        X = points[:, 0]
        Y = points[:, 1]
        Z = np.zeros(len(points))
        Z2 = np.full(len(points), 5000)  # height is 5 meters (5000 mm)

        # Create closed polyline by connecting the points
        for i in range(len(points) - 1):
            color = cm.viridis(Z[i] / 5000)  # Using Viridis colormap
            self.ax3d.plot([points[i][0], points[i + 1][0]],
                           [points[i][1], points[i + 1][1]], [0, 0], color=color, linewidth=2.0)
            self.ax3d.plot([points[i][0], points[i + 1][0]],
                           [points[i][1], points[i + 1][1]], [5000, 5000], color=color, linewidth=2.0)
            self.ax3d.plot([points[i][0], points[i][0]],
                           [points[i][1], points[i][1]], [0, 5000], color=color, linewidth=2.0)

        # Connect the last point to the first to close the polyline
        color = cm.viridis(Z[-1] / 5000)  # Color for the last segment
        self.ax3d.plot([points[-1][0], points[0][0]],
                       [points[-1][1], points[0][1]], [0, 0], color=color, linewidth=2.0)
        self.ax3d.plot([points[-1][0], points[0][0]],
                       [points[-1][1], points[0][1]], [5000, 5000], color=color, linewidth=2.0)
        self.ax3d.plot([points[-1][0], points[-1][0]],
                       [points[-1][1], points[-1][1]], [0, 5000], color=color, linewidth=2.0)

        self.ax3d.set_xlabel('X (mm)')
        self.ax3d.set_ylabel('Y (mm)')
        self.ax3d.set_zlabel('Z (mm)')

        # Create a canvas to display the figure
        self.canvas = FigureCanvas(fig)

        # Create a navigation toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Create a QFrame to hold canvas and toolbar
        frame = QtWidgets.QFrame()
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)

        # Create a layout for the QFrame
        frame_layout = QtWidgets.QVBoxLayout(frame)
        frame_layout.addWidget(self.toolbar)
        frame_layout.addWidget(self.canvas)

        # Set the layout to stretch the canvas
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)
        frame.setLayout(frame_layout)

        # Set the central widget to the QFrame
        self.setCentralWidget(frame)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())
