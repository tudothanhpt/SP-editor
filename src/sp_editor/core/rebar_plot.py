from PySide6 import QtWidgets as qtw
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from sp_editor.core.mpl_canvas import MplCanvas


def plot_polygons(frame: qtw.QFrame, polygons, shapes, rebar_list):
    """
    Plots a list of Shapely polygons using Matplotlib.

    :param frame: The QFrame object to embed the plot in.
    :param polygons: List of Shapely Polygon objects to be plotted.
    :param shapes: List of shapes to be plotted.
    :param rebar_list: List of rebar coordinates to be plotted.
    """
    # Create or get the canvas
    if not hasattr(frame, "canvas"):
        # Create a Matplotlib figure
        frame.canvas = MplCanvas(frame, width=14, height=12, dpi=100)
        frame.toolbar = NavigationToolbar(frame.canvas, frame)

        # Create a layout for the QFrame
        frame.layout = qtw.QVBoxLayout()
        frame.layout.addWidget(frame.toolbar)
        frame.layout.addWidget(frame.canvas)
        frame.setLayout(frame.layout)
    else:
        frame.canvas.axes.clear()

    ax = frame.canvas.axes

    for polygon in polygons:
        x, y = zip(*polygon)
        # ax.plot(x, y, color='b', linewidth=1, linestyle='--')

    for shape in shapes:
        x, y = zip(*shape)
        ax.plot(x, y, color="r", linewidth=1.5)

    x, y = zip(*rebar_list)
    ax.scatter(x, y, color="g", s=1)

    ax.set_title("Cross Section")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    # Automatically set limits
    all_x = (
        [coord[0] for polygon in polygons for coord in polygon]
        + [coord[0] for shape in shapes for coord in shape]
        + [coord[0] for coord in rebar_list]
    )
    all_y = (
        [coord[1] for polygon in polygons for coord in polygon]
        + [coord[1] for shape in shapes for coord in shape]
        + [coord[1] for coord in rebar_list]
    )

    ax.set_xlim(min(all_x) - 100, max(all_x) + 100)
    ax.set_ylim(min(all_y) - 100, max(all_y) + 100)

    # Trigger the canvas to update and redraw.
    frame.canvas.draw()
