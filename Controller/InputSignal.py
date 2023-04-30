class InputSignal:

    def __init__(self):
        self.offset = 0
        self.frequency = 60
        self.amplitude = 5

    def get_signal_data(self):
        return self.frequency, self.offset, self.amplitude

    def print_signal_data(self):
        print ("Amplitude:{0}\nOffset:{1}\nFrequency:{2}".format (str (self.amplitude), str (self.offset), str (
            self.frequency)))
