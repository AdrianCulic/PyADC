from PyQt5.QtWidgets import QMainWindow

from Controller.MatplotlibCanvas import MplCanvas
from Controller.InputSignal import InputSignal
from Controller.DetailedSigButton import DetailedSigButton as dsb
from Controller.SetupSpecs import SetupSpec as ss
from Controller.ADCData import ADCData
from View import view as ProjectView
import numpy as np
from scipy import signal
from PyQt5 import QtGui


def info_button_pressed():
    message_button = dsb()


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = ProjectView.Ui_MainWindow()
        self.ui.setupUi(self)
        self.sc = MplCanvas(self, width=15, height=3, dpi=100)
        self.ui.PlotLayout.addWidget(self.sc)
        self.ref_signal_data = InputSignal()
        self.convertor_data = ADCData()
        self.output_montage = ss()
        self.previousGraphType = 0  # sinus default
        self.div_mult = 1
        self.div_cf_val = 1
        self.div_val = 5
        self.t = 5
        self.graph_dt = 0.001
        self.signal_generator_type = 0
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
        self.ui.checkBox.stateChanged.connect(self.constant_signal_checkbox_event)
        self.ui.InfoPushButton.pressed.connect(info_button_pressed)
        self.ui.comboBoxBitNo.activated.connect(self.bit_no_changed)
        self.ui.lineEdiRech.returnPressed.connect(self.r_ech_chagned)
        self.ui.lineEditRespTime.editingFinished.connect(self.response_time_changed)
        self.ui.lineEditVref.returnPressed.connect(self.v_ref_changed)
        self.ui.lineEditIrefLim.returnPressed.connect(self.i_ref_changed)
        self.ui.comboBoxClockT.activated.connect(self.clock_time_changed)
        self.ui.comboBoxEvoSigType.activated.connect(self.evo_type_changed)
        self.ui.lineEditSRAO.editingFinished.connect(self.slew_rate_changed)
        self.ui.lineEditRout.editingFinished.connect(self.r_out_changed)

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
        # sinus
        if self.ui.checkBox.isChecked():
            self.plot_constant_signal()
        else:
            if x == 0:
                self.plot_rectangular()
            elif x == 1:
                self.plot_sinus()
            else:
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
        self.ui.lineEdiRech.setText(str(self.convertor_data.ech_R))
        self.ui.lineEditRespTime.setText(str(self.convertor_data.response_time))
        self.ui.lineEditVref.setText(str(self.convertor_data.V_lim))
        self.ui.lineEdiRech.setText(str(self.convertor_data.R_ref))
        self.ui.lineEditIrefLim.setText(str(self.convertor_data.I_ref))
        self.ui.lineEditRout.setText(str(self.output_montage.R_out))
        self.ui.lineEditSRAO.setText(str(self.output_montage.SR_opAmp))

    def time_unit_changed(self):
        x = self.ui.UnitTypeComboBox.currentIndex()
        if x == 0:
            self.div_cf_val = 1
        elif x == 1:
            self.div_cf_val = 0.001
        elif x == 2:
            self.div_cf_val = 0.000001
        else:
            self.div_cf_val = 0.000000001
        self.calculate_x_div_value()
        self.wave_changed()

    def change_dt(self):
        self.graph_dt = self.div_cf_val / 10000

    def plot_constant_signal(self):
        self.sc.axes.hlines(self.ref_signal_data.amplitude, xmax=self.div_val, xmin=0)
        self.sc.axes.plot()
        self.sc.figure.canvas.draw()

    def constant_signal_checkbox_event(self):
        if self.ui.checkBox.isChecked():
            self.ui.lineEditFreq.setDisabled(True)
            self.ui.lineEditOff.setDisabled(True)
            self.ui.comboBoxSigType.setDisabled(True)
            self.ui.label_3.setText("Valoare CC:")
        else:
            self.ui.lineEditFreq.setDisabled(False)
            self.ui.lineEditOff.setDisabled(False)
            self.ui.comboBoxSigType.setDisabled(False)
            self.ui.label_3.setText("Amplitudine")
        self.wave_changed()

    def bit_no_changed(self):
        bit_convertor = 6
        if self.ui.comboBoxBitNo.currentIndex() == 0:
            bit_convertor = 6
        elif self.ui.comboBoxBitNo.currentIndex() == 1:
            bit_convertor = 7
        elif self.ui.comboBoxBitNo.currentIndex() == 2:
            bit_convertor = 8
        elif self.ui.comboBoxBitNo.currentIndex() == 3:
            bit_convertor = 9
        self.convertor_data.bits_no = bit_convertor
        print(self.convertor_data.bits_no)
        self.wave_changed()

    def r_ech_chagned(self):
        self.convertor_data.R_ref = float(self.ui.lineEdiRech.displayText())
        self.convertor_data.I_ref = self.convertor_data.V_lim / self.convertor_data.R_ref * 1000
        self.init_line_text()
        self.wave_changed()

    def response_time_changed(self):
        self.convertor_data.response_time = float(self.ui.lineEdiRech.displayText())
        self.wave_changed()

    def i_ref_changed(self):
        self.convertor_data.I_ref = float(self.ui.lineEditIrefLim.displayText())
        self.convertor_data.V_lim = self.convertor_data.R_ref * (self.convertor_data.I_ref/1000)
        self.init_line_text()  # update text for lineEdits
        self.wave_changed()

    def v_ref_changed(self):
        self.convertor_data.V_lim = float(self.ui.lineEditVref.displayText())
        self.convertor_data.I_ref = self.convertor_data.V_lim / self.convertor_data.R_ref * 1000
        self.init_line_text()
        self.wave_changed()

    def r_out_changed(self):
        self.output_montage.R_out = float(self.ui.lineEditRout.displayText())
        self.wave_changed()

    def slew_rate_changed(self):
        self.output_montage.SR_opAmp = float(self.ui.lineEditSRAO.displayText())
        self.wave_changed()

    def clock_time_changed(self):
        self.output_montage.clock_idx = self.ui.comboBoxClockT.currentIndex()
        self.output_montage.set_clock_timer_base()
        self.wave_changed()

    def evo_type_changed(self):
        sig_gen_type = self.ui.comboBoxSigType.currentIndex()
        if sig_gen_type == 0:
            self.signal_generator_type = 0
        else:
            self.signal_generator_type = 1
        self.wave_changed()

