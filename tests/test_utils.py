import sys
import math
import pandas as pd
import plotly.graph_objects as go
from PySide6.QtCore import QUrl, QTimer, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QPushButton, \
    QLineEdit, QLabel, QStatusBar, QProgressBar
from PySide6.QtWebEngineWidgets import QWebEngineView
from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:')  # Replace with your actual engine


def get_rebarCoordinates_str(frame: QFrame, engine, cover: float, bar_area: float, spacing: float, SDname: str):
    bar_dia = math.sqrt(bar_area / math.pi) * 2
    offset_distance = (cover + (bar_dia / 2)) * (-1)
    rebarArea = bar_area

    df_sd = pd.DataFrame()  # Mock: replace with read_sdsDB(engine)
    lst_PierSDShape = []  # Mock: replace with restructure_sdshapeDF(df_sd)
    idx = 0  # Mock: replace with find_key_index(lst_PierSDShape, SDname)
    PierSDShape = []  # Mock: replace with actual data

    offsetted_shapes = []  # Mock: replace with offset_sdshapeDF(lst_PierSDShape, SDname, offset_distance)
    rebar_list = [(0, 0)]  # Mock: replace with calculate_rebarpoints_for_segments(offsetted_shapes, spacing)
    total_rebar, multiline_string_rebarPts = 0, ""  # Mock: replace with spColumn_CTI_Rebar(rebar_list, rebarArea)
    plot_polygons(frame, offsetted_shapes, PierSDShape, rebar_list)
    return total_rebar, multiline_string_rebarPts


def plot_polygons(frame: QFrame, polygons, shapes, rebar_list):
    """
    Plots a list of polygons using Plotly and embeds it into a QWebEngineView.

    :param frame: The QFrame object to embed the plot in.
    :param polygons: List of polygon coordinates to be plotted.
    :param shapes: List of shape coordinates to be plotted.
    :param rebar_list: List of rebar coordinates to be plotted.
    """
    # Get the dimensions of the QFrame
    frame_width = frame.size().width()
    frame_height = frame.size().height()

    # Create a Plotly figure
    fig = go.Figure()

    for polygon in polygons:
        x, y = zip(*polygon)
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='blue', dash='dash')))

    for shape in shapes:
        x, y = zip(*shape)
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='red', width=1.5)))

    if rebar_list:
        x, y = zip(*rebar_list)
        fig.add_trace(go.Scatter(x=x, y=y, mode='markers', marker=dict(color='green', size=5)))

    fig.update_layout(
        title='Cross Section',
        xaxis_title='X',
        yaxis_title='Y',
        showlegend=False,
        width=frame_width,
        height=frame_height
    )

    # Convert Plotly figure to HTML
    html = fig.to_html(include_plotlyjs='cdn')

    # Create or get the QWebEngineView
    if not hasattr(frame, 'webview'):
        frame.webview = QWebEngineView()
        frame.layout = QVBoxLayout()
        frame.layout.addWidget(frame.webview)
        frame.setLayout(frame.layout)

    # Set HTML content in QWebEngineView
    frame.webview.setHtml(html)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.frame = QFrame(self)

        self.cover_input = QLineEdit(self)
        self.bar_area_input = QLineEdit(self)
        self.spacing_input = QLineEdit(self)
        self.sdname_input = QLineEdit(self)
        self.update_button = QPushButton('Update Plot', self)

        self.cover_input.setText('50')
        self.bar_area_input.setText('200')
        self.spacing_input.setText('100')
        self.sdname_input.setText('SD1')

        self.update_button.clicked.connect(self.update_plot)

        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel('Cover:'))
        input_layout.addWidget(self.cover_input)
        input_layout.addWidget(QLabel('Bar Area:'))
        input_layout.addWidget(self.bar_area_input)
        input_layout.addWidget(QLabel('Spacing:'))
        input_layout.addWidget(self.spacing_input)
        input_layout.addWidget(QLabel('SD Name:'))
        input_layout.addWidget(self.sdname_input)
        input_layout.addWidget(self.update_button)

        layout = QVBoxLayout()
        layout.addLayout(input_layout)
        layout.addWidget(self.frame)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Add status bar and progress bar
        self.status_bar = QStatusBar()
        self.progress_bar = QProgressBar()
        self.status_bar.addPermanentWidget(self.progress_bar)
        self.setStatusBar(self.status_bar)

        self.setWindowTitle("Rebar Coordinates and Cross Section Plot")
        self.setGeometry(100, 100, 800, 600)

        self.update_plot()

    def update_plot(self):
        cover = float(self.cover_input.text())
        bar_area = float(self.bar_area_input.text())
        spacing = float(self.spacing_input.text())
        sdname = self.sdname_input.text()

        # Simulate progress for demonstration purposes
        self.progress_bar.setValue(0)
        QTimer.singleShot(100, lambda: self.progress_bar.setValue(25))
        QTimer.singleShot(200, lambda: self.progress_bar.setValue(50))
        QTimer.singleShot(300, lambda: self.progress_bar.setValue(75))
        QTimer.singleShot(400, lambda: self.progress_bar.setValue(100))

        total_rebar, multiline_string_rebarPts = get_rebarCoordinates_str(self.frame, engine, cover, bar_area, spacing,
                                                                          sdname)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
