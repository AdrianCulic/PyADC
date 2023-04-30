from PyQt5.QtWidgets import QMainWindow

from Controller.MatplotlibCanvas import MplCanvas
from Controller.InputSignal import InputSignal

from View import view as ProjectView
import numpy as np
from scipy import signal
from PyQt5 import QtGui


class Window (QMainWindow):
    def __init__(self, parent=None):
        super ().__init__ (parent)
        self.ui = ProjectView.Ui_MainWindow ()
        self.ui.setupUi (self)
        self.sc = MplCanvas (self, width=15, height=3, dpi=100)
        self.ui.PlotLayout.addWidget (self.sc)
        self.ref_signal_data = InputSignal ()
        self.previousGraphType = 0  # sinus default
        self.init_plot ()
        self.link_events ()

    def link_events(self):
        self.ui.comboBoxSigType.activated.connect (self.wave_changed)
        self.ui.comboBoxSchemeType.activated.connect (self.label_image_changed)
        self.ui.lineEditOff.returnPressed.connect (self.update_offset)
        self.ui.lineEditFreq.returnPressed.connect (self.update_frequency)
        self.ui.lineEditAmplt.returnPressed.connect (self.update_amplitude)

    def init_plot(self):
        self.sc.axes.grid (color='red', linestyle='--', linewidth=0.5)
        self.sc.axes.set_facecolor ("black")
        # adjust for the max value
        self.sc.axes.set_xlim (left=0, right=5)

    def plot_rectangular(self):
        dt = 0.001  # sampling interval
        t = np.arange (0, 1, dt)
        signal_to_plot = self.ref_signal_data.offset + \
                         self.ref_signal_data.amplitude * \
                         signal.square (2 * np.pi *self.ref_signal_data.frequency * t)
        self.sc.axes.plot (t, signal_to_plot)
        self.sc.figure.canvas.draw()

    def plot_triangular(self):
        t = np.linspace (0, 1, 500, endpoint=False)
        self.sc.axes.plot (t, signal.sawtooth (2 * np.pi * 5 * t, width=0.5))
        self.sc.figure.canvas.draw ()

    def plot_sinus(self):
        t = np.linspace (0, 1, 500, endpoint=False)
        self.sc.axes.plot (t, np.sin (2 * np.pi * 5 * t))
        self.sc.figure.canvas.draw ()

    def clear_graph(self):
        self.sc.axes.cla()
        self.init_plot()

    def label_image_changed(self):
        x = self.ui.comboBoxSchemeType.currentIndex ()
        if x == 0:
            self.ui.labelImage.setPixmap (QtGui.QPixmap("Bipolar_Iout_ss.png"))
        elif x == 1:
            self.ui.labelImage.setPixmap (QtGui.QPixmap("Bipolar_Vout_ss.png"))
        elif x == 2:
            self.ui.labelImage.setPixmap (QtGui.QPixmap("CMOS_SS.png"))

    def wave_changed(self):
        x = self.ui.comboBoxSigType.currentIndex ()
        self.clear_graph()
        print (x)
        # sinus
        if x == 0:
            self.plot_rectangular ()
        elif x == 1:
            self.plot_sinus ()
        elif x == 2:
            self.plot_triangular ()

    def update_offset(self):
        self.ref_signal_data.offset = int (self.ui.lineEditOff.displayText ())
        self.ref_signal_data.print_signal_data ()
        self.wave_changed()

    def update_amplitude(self):
        self.ref_signal_data.amplitude = int (self.ui.lineEditAmplt.displayText ())
        self.ref_signal_data.print_signal_data ()
        self.wave_changed ()

    def update_frequency(self):
        self.ref_signal_data.frequency = int (self.ui.lineEditFreq.displayText ())
        self.ref_signal_data.print_signal_data ()
        self.wave_changed ()
