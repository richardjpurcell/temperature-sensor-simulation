class Transducer:
    """Simulates a transducer capturing temperature data."""
    def __init__(self, simulator, time, samples_per_day=24):
        self.simulator = simulator
        self.time = time
        self.sample_interval = 1440 / samples_per_day  # Interval in minutes
        self.last_sample_time = -self.sample_interval  # Initialize before the start time
        self.captured_data = []

    def set_samples_per_day(self, samples_per_day):
        """Update the sampling rate by setting samples per day."""
        self.sample_interval = 1440 / samples_per_day  # Recalculate the sampling interval

    def capture(self):
        """Capture temperature if the sample interval has elapsed."""
        current_time_minutes = self.time.get_current_time() / 60  # Convert seconds to minutes
        if current_time_minutes - self.last_sample_time >= self.sample_interval:
            temperature = self.simulator.generate_temperature(current_time_minutes / 1440)  # Fraction of a day
            self.last_sample_time = current_time_minutes
            self.captured_data.append((current_time_minutes, temperature))
            return temperature
        return None
