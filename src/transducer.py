class Transducer:
    """Simulates a transducer capturing temperature data."""
    def __init__(self, simulator, samples_per_day=24):
        self.simulator = simulator
        self.samples_per_day = samples_per_day
        self.captured_data = []

    def set_samples_per_day(self, value):
        self.samples_per_day = value

    def capture(self, time):
        """Capture the temperature at the current time."""
        interval = 1 / self.samples_per_day  # Time interval for each sample
        last_sample_time = self.captured_data[-1][0] if self.captured_data else -interval
        if time - last_sample_time >= interval:
            temperature = self.simulator.generate_temperature(time)
            self.captured_data.append((time, temperature))
            return temperature
        return None
