from matplotlib.backends.backend_qt5agg import *
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=100, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.subplots_adjust (left=0.06, bottom=0.09, right=0.99, top=0.97, wspace=0, hspace=0.01)
        super(MplCanvas, self).__init__(fig)