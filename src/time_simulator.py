

class Time:
    """Manages the simulation time."""
    def __init__(self, start_time=0, increment=1):
        self.current_time = start_time  # Initialize with a starting time
        self.increment = increment  # Time step increment in seconds

    def advance(self):
        """Advance the current time by the increment."""
        self.current_time += self.increment

    def reset(self):
        """Reset the time to the start."""
        self.current_time = 0

    def get_current_time(self):
        """Return the current time."""
        return self.current_time

