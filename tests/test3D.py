from PySide6 import QtCore, QtGui, QtWidgets
import numpy as np
from matplotlib import cm
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d.axes3d import get_test_data
from matplotlib.figure import Figure


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Plot Example")
        self.setGeometry(100, 100, 800, 600)

        # Create a Matplotlib figure
        fig = Figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.set_axis_off()
        # Add your 3D plot data here (e.g., scatter, surface, etc.)
        # plot a 3D surface like in the example mplot3d/surface3d_demo
        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X ** 2 + Y ** 2)
        Z = np.sin(R)
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)
        ax.set_zlim(-1.01, 1.01)
        fig.colorbar(surf, shrink=0.5, aspect=10)

        # Create a canvas to display the figure
        canvas = FigureCanvas(fig)
        self.setCentralWidget(canvas)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec()
