from PyQt5.QtWidgets import QMainWindow

from Controller.MatplotlibCanvas import MplCanvas
from Controller.InputSignal import InputSignal

from View import view as ProjectView
import numpy as np
from scipy import signal
from PyQt5 import QtGui


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = ProjectView.Ui_MainWindow()
        self.ui.setupUi(self)
        self.sc = MplCanvas(self, width=15, height=3, dpi=100)
        self.ui.PlotLayout.addWidget(self.sc)
        self.ref_signal_data = InputSignal()
        self.previousGraphType = 0  # sinus default
        self.div_mult = 1
        self.div_cf_val = 1
        self.div_val = 5
        self.t = 5
        self.graph_dt = 0.001
        self.init_plot()
        self.calculate_x_div_value()
        self.link_events()
        self.init_line_text()
        self.wave_changed()

    def link_events(self):
        self.ui.comboBoxSigType.activated.connect(self.wave_changed)
        self.ui.comboBoxSchemeType.activated.connect(self.label_image_changed)
        self.ui.lineEditOff.editingFinished.connect(self.update_offset)
        self.ui.lineEditFreq.editingFinished.connect(self.update_frequency)
        self.ui.lineEditAmplt.editingFinished.connect(self.update_amplitude)
        self.ui.DivNoSpinBox.valueChanged.connect(self.spinbox_value_changed)
        self.ui.UnitTypeComboBox.currentTextChanged.connect(self.time_unit_changed)

    def init_plot(self):
        self.sc.axes.grid(color='red', linestyle='--', linewidth=0.5)
        self.sc.axes.set_facecolor("black")
        self.sc.axes.set_xlim(left=0, right=self.div_val)

    def arrange_axis(self):
        self.t = np.arange(0, self.div_val, self.graph_dt)

    def plot_rectangular(self):
        signal_to_plot = self.ref_signal_data.offset +\
                         self.ref_signal_data.amplitude *\
                         signal.square(2 * np.pi * self.ref_signal_data.frequency * self.t)
        self.sc.axes.plot(self.t, signal_to_plot)
        self.sc.figure.canvas.draw()

    def plot_triangular(self):
        signal_to_plot = self.ref_signal_data.offset +\
                         self.ref_signal_data.amplitude *\
                         signal.sawtooth(2 * np.pi * 5 * self.t, width=0.5)
        self.sc.axes.plot(self.t, signal_to_plot)
        self.sc.figure.canvas.draw()

    def plot_sinus(self):
        signal_to_plot = self.ref_signal_data.offset +\
                         self.ref_signal_data.amplitude *\
                         np.sin(2 * np.pi * 5 * self.t)
        self.sc.axes.plot(self.t, signal_to_plot)
        self.sc.figure.canvas.draw()

    def clear_graph(self):
        self.sc.axes.cla()
        self.init_plot()
        self.change_dt()

    def label_image_changed(self):
        x = self.ui.comboBoxSchemeType.currentIndex()
        if x == 0:
            self.ui.labelImage.setPixmap(QtGui.QPixmap("Bipolar_Iout_ss.png"))
        elif x == 1:
            self.ui.labelImage.setPixmap(QtGui.QPixmap("Bipolar_Vout_ss.png"))
        elif x == 2:
            self.ui.labelImage.setPixmap(QtGui.QPixmap("CMOS_SS.png"))

    def wave_changed(self):
        x = self.ui.comboBoxSigType.currentIndex()
        self.clear_graph()
        self.arrange_axis()
        print(x)
        # sinus
        if x == 0:
            self.plot_rectangular()
        elif x == 1:
            self.plot_sinus()
        elif x == 2:
            self.plot_triangular()

    def update_offset(self):
        self.ref_signal_data.offset = int(self.ui.lineEditOff.displayText())
        self.ref_signal_data.print_signal_data()
        self.wave_changed()

    def update_amplitude(self):
        self.ref_signal_data.amplitude = int(self.ui.lineEditAmplt.displayText())
        self.ref_signal_data.print_signal_data()
        self.wave_changed()

    def update_frequency(self):
        self.ref_signal_data.frequency = int(self.ui.lineEditFreq.displayText())
        self.ref_signal_data.print_signal_data()
        self.wave_changed()

    def spinbox_value_changed(self):
        self.div_mult = self.ui.DivNoSpinBox.value()
        self.calculate_x_div_value()
        self.wave_changed()

    def calculate_x_div_value(self):
        self.div_val = self.div_cf_val * self.div_mult

    def init_line_text(self):
        self.ui.lineEditOff.setText(str(self.ref_signal_data.offset))
        self.ui.lineEditFreq.setText(str(self.ref_signal_data.frequency))
        self.ui.lineEditAmplt.setText(str(self.ref_signal_data.amplitude))

    def time_unit_changed(self):
        x = self.ui.UnitTypeComboBox.currentIndex()
        if x == 0:
            self.div_cf_val = 1
        elif x == 1:
            self.div_cf_val = 0.01
        elif x == 2:
            self.div_cf_val = 0.000001
        else:
            self.div_cf_val = 0.000000001
        self.calculate_x_div_value()
        self.wave_changed()

    def change_dt(self):
        self.graph_dt = self.div_cf_val / 10000
