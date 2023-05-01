class ADCData:
    def __init__(self):
        self.bits_no = 6
        self.response_time = 100  # ns 1 - 10000
        self.ech_R = 1000  # default resistance
        self.V_lim = 15
        self.I_ref = 15  # mA
        self.R_ref = 1000
