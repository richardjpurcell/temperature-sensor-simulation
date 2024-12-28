import numpy as np

class TemperatureSimulator:
    """Simulates the temperature at a specific point (x, y)."""
    def __init__(self, min_temp=3, max_temp=18):
        self.min_temp = min_temp
        self.max_temp = max_temp

    def set_min_temp(self, value):
        self.min_temp = value

    def set_max_temp(self, value):
        self.max_temp = value

    def generate_temperature(self, time):
        """Generate realistic temperature fluctuations using a sine wave model."""
        midday_peak = 16  # Peak temperature at 16:00 (4 PM)
        hour = (time % 1) * 24  # Fractional part of the day converted to hours
        temp_amplitude = (self.max_temp - self.min_temp) / 2
        base_temp = (self.max_temp + self.min_temp) / 2
        return base_temp + temp_amplitude * np.sin((hour - midday_peak) * np.pi / 12)
