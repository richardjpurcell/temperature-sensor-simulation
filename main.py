import sys
from PyQt5.QtWidgets import QApplication
from src.temperature_visualizer import TemperatureVisualizer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TemperatureVisualizer()
    window.show()
    sys.exit(app.exec_())
