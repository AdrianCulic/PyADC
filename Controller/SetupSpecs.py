class SetupSpec:
    def __init__(self):
        self.R_out = 10
        self.SR_opAmp = 1 #[V/ms] 0.1 - 100
        self.clock_timer_base = [0.1, 0.3, 1, 3, 10]
        self.clock_idx = 0
        self.clock_time = 1

    def set_clock_timer_base(self):
        self.clock_time = self.clock_timer_base[self.clock_idx]

