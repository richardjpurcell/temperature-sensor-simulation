from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg
from src.temperature_simulator import TemperatureSimulator
from src.transducer import Transducer

class TemperatureVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Temperature Simulation with Transducer")
        self.resize(800, 600)

        # Main layout
        self.main_widget = QWidget()
        self.layout = QVBoxLayout(self.main_widget)

        # PyQtGraph plot widgets
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('left', "Temperature (°C)")
        self.plot_widget.setLabel('bottom', "Days")
        self.layout.addWidget(self.plot_widget)
        self.plot = self.plot_widget.plot()

        self.transducer_plot = pg.PlotWidget()
        self.transducer_plot.setLabel('left', "Transducer Data (°C)")
        self.transducer_plot.setLabel('bottom', "Days")
        self.layout.addWidget(self.transducer_plot)
        self.transducer_curve = self.transducer_plot.plot()

        # Current day label
        self.day_label = QLabel("Current Day: 1")
        self.day_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.day_label)

        # Sliders for min and max temperatures
        slider_layout = QHBoxLayout()

        self.min_temp_label = QLabel("Min Temp: 3°C")
        self.max_temp_label = QLabel("Max Temp: 18°C")

        self.min_temp_slider = QSlider(Qt.Horizontal)
        self.min_temp_slider.setRange(-10, 15)
        self.min_temp_slider.setValue(3)
        self.min_temp_slider.valueChanged.connect(self.update_min_temp)

        self.max_temp_slider = QSlider(Qt.Horizontal)
        self.max_temp_slider.setRange(10, 40)
        self.max_temp_slider.setValue(18)
        self.max_temp_slider.valueChanged.connect(self.update_max_temp)

        slider_layout.addWidget(self.min_temp_label)
        slider_layout.addWidget(self.min_temp_slider)
        slider_layout.addWidget(self.max_temp_label)
        slider_layout.addWidget(self.max_temp_slider)

        # Slider for samples per day
        self.samples_per_day_label = QLabel("Samples/Day: 24")
        self.samples_per_day_slider = QSlider(Qt.Horizontal)
        self.samples_per_day_slider.setRange(1, 144)
        self.samples_per_day_slider.setValue(24)
        self.samples_per_day_slider.valueChanged.connect(self.update_samples_per_day)
        slider_layout.addWidget(self.samples_per_day_label)
        slider_layout.addWidget(self.samples_per_day_slider)

        self.layout.addLayout(slider_layout)
        self.setCentralWidget(self.main_widget)

        # Initialize simulator and transducer
        self.simulator = TemperatureSimulator()
        self.transducer = Transducer(self.simulator)

        # Initialize data
        self.x_range = 3
        self.x = []
        self.temperatures = []
        self.transducer_times = []
        self.transducer_temps = []
        self.scroll_offset = 0
        self.current_day = 1

        # Timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_temperature)
        self.timer.start(50)

    def update_min_temp(self, value):
        self.simulator.set_min_temp(value)
        self.min_temp_label.setText(f"Min Temp: {value}°C")

    def update_max_temp(self, value):
        self.simulator.set_max_temp(value)
        self.max_temp_label.setText(f"Max Temp: {value}°C")

    def update_samples_per_day(self, value):
        self.transducer.set_samples_per_day(value)
        self.samples_per_day_label.setText(f"Samples/Day: {value}")

    def update_temperature(self):
        self.scroll_offset += 0.1
        if self.scroll_offset >= 24:
            self.scroll_offset = 0
            self.current_day += 1
            self.day_label.setText(f"Current Day: {self.current_day}")

        new_time = (self.current_day - 1) + self.scroll_offset / 24
        new_temperature = self.simulator.generate_temperature(new_time)

        self.x.append(new_time)
        self.temperatures.append(new_temperature)

        transducer_temp = self.transducer.capture(new_time)
        if transducer_temp is not None:
            self.transducer_times.append(new_time)
            self.transducer_temps.append(transducer_temp)

        if len(self.x) > self.x_range * 1000:
            self.x.pop(0)
            self.temperatures.pop(0)

        self.plot.setData(self.x, self.temperatures)
        self.transducer_curve.setData(self.transducer_times, self.transducer_temps)
        self.plot_widget.setXRange(self.x[-1] - self.x_range, self.x[-1])
        self.transducer_plot.setXRange(self.x[-1] - self.x_range, self.x[-1])
