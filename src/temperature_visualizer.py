from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg
import numpy as np
from scipy.interpolate import interp1d
from src.temperature_simulator import TemperatureSimulator
from src.time_simulator import Time
from src.transducer import Transducer

class TemperatureVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Temperature Simulation with Transducer")
        self.resize(800, 800)  # Increased height for two plots

        # Main layout
        self.main_widget = QWidget()
        self.layout = QVBoxLayout(self.main_widget)

        # PyQtGraph plot widget for actual temperature
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('left', "Temperature (°C)")
        self.plot_widget.setLabel('bottom', "Minutes")
        self.layout.addWidget(self.plot_widget)
        self.plot = self.plot_widget.plot()

        # PyQtGraph plot widget for transducer output
        self.transducer_plot_widget = pg.PlotWidget()
        self.transducer_plot_widget.setLabel('left', "Transducer Temp (°C)")
        self.transducer_plot_widget.setLabel('bottom', "Minutes")
        self.layout.addWidget(self.transducer_plot_widget)
        self.transducer_plot = self.transducer_plot_widget.plot()

        # Current time label
        self.time_label = QLabel("Current Time: 0 minutes")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.time_label)

        # Sampling rate slider
        self.sampling_rate_label = QLabel("Sampling Rate: 60 minutes/sample")
        self.layout.addWidget(self.sampling_rate_label)

        self.sampling_rate_slider = QSlider(Qt.Horizontal)
        self.sampling_rate_slider.setRange(1, 1440)  # 1 minute to 1 day (1440 minutes)
        self.sampling_rate_slider.setValue(60)  # Default to 60 minutes/sample
        self.sampling_rate_slider.valueChanged.connect(self.update_sampling_rate)
        self.layout.addWidget(self.sampling_rate_slider)

        self.setCentralWidget(self.main_widget)

        # Initialize simulator, time, and transducer
        self.time = Time(start_time=0, increment=60)  # Increment by 1 minute
        self.simulator = TemperatureSimulator()
        self.transducer = Transducer(self.simulator, self.time, samples_per_day=24)  # 60-minute sampling

        # Initialize data
        self.x_range = 1440  # Visible range in minutes (24 hours)
        self.x = []  # X-axis data for actual temperature
        self.temperatures = []  # Y-axis data for actual temperature
        self.transducer_times = []  # X-axis data for transducer output
        self.transducer_temps = []  # Y-axis data for transducer output

        # Timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(6)  # Faster scrolling with a 6 ms interval

    def update_sampling_rate(self, value):
        """Update the sampling rate of the transducer."""
        samples_per_day = 1440 // value  # Calculate samples per day based on minutes/sample
        self.transducer.set_samples_per_day(samples_per_day)
        self.sampling_rate_label.setText(f"Sampling Rate: {value} minutes/sample")

    def update_simulation(self):
        """Update the temperature simulation and interpolate transducer output."""
        self.time.advance()
        current_time_seconds = self.time.get_current_time()
        current_time_minutes = current_time_seconds / 60  # Convert seconds to minutes

        # Update label
        self.time_label.setText(f"Current Time: {int(current_time_minutes)} minutes")

        # Generate new temperature
        new_temperature = self.simulator.generate_temperature(current_time_seconds / 86400)  # Convert seconds to fraction of a day
        self.x.append(current_time_minutes)
        self.temperatures.append(new_temperature)

        # Transducer sampling
        transducer_temp = self.transducer.capture()
        if transducer_temp is not None:
            self.transducer_times.append(current_time_minutes)
            self.transducer_temps.append(transducer_temp)

        # Interpolation for smooth scrolling
        if len(self.transducer_times) > 1:
            interpolation_func = interp1d(self.transducer_times, self.transducer_temps, kind="linear", fill_value="extrapolate")
            interpolated_times = np.linspace(self.transducer_times[0], self.transducer_times[-1], len(self.x))
            interpolated_temps = interpolation_func(interpolated_times)
        else:
            interpolated_times = self.transducer_times
            interpolated_temps = self.transducer_temps

        # Remove old data to maintain scrolling
        if len(self.x) > self.x_range:
            self.x = self.x[-self.x_range:]
            self.temperatures = self.temperatures[-self.x_range:]
        if len(self.transducer_times) > self.x_range:
            self.transducer_times = self.transducer_times[-self.x_range:]
            self.transducer_temps = self.transducer_temps[-self.x_range:]

        # Update the plots
        self.plot.setData(self.x, self.temperatures)
        self.transducer_plot.setData(interpolated_times, interpolated_temps)

        # Update the visible range to scroll
        self.plot_widget.setXRange(self.x[-1] - self.x_range, self.x[-1])
        self.transducer_plot_widget.setXRange(self.x[-1] - self.x_range, self.x[-1])

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = TemperatureVisualizer()
    window.show()
    sys.exit(app.exec_())
