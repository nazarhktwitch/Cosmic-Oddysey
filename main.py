import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QSlider, QPushButton, QLineEdit, QTabWidget
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QPalette, QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class CosmicOdyssey(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon('icon.ico'))

        # Window setup
        self.setWindowTitle("Cosmic Odyssey")
        self.setGeometry(100, 100, 800, 600)

        # Set cosmic theme
        self.set_cosmic_theme()

        # Main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Tab widget for different sections
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background: #2E3440;
                color: #D8DEE9;
                padding: 10px;
                border: 1px solid #4C566A;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #4C566A;
                color: #ECEFF4;
            }
        """)
        self.layout.addWidget(self.tabs)

        # Add tabs
        self.add_intelligent_life_tab()
        self.add_asteroid_collision_tab()

        # Add smooth fade-in animation
        self.fade_in_animation()

    def set_cosmic_theme(self):
        """Set a cosmic-themed color palette."""
        cosmic_palette = QPalette()
        cosmic_palette.setColor(QPalette.ColorRole.Window, QColor(46, 52, 64))  # Dark background
        cosmic_palette.setColor(QPalette.ColorRole.WindowText, QColor(216, 222, 233))  # Light text
        cosmic_palette.setColor(QPalette.ColorRole.Button, QColor(76, 86, 106))  # Button background
        cosmic_palette.setColor(QPalette.ColorRole.ButtonText, QColor(216, 222, 233))  # Button text
        cosmic_palette.setColor(QPalette.ColorRole.Highlight, QColor(129, 161, 193))  # Highlight color
        cosmic_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(46, 52, 64))  # Highlighted text
        self.setPalette(cosmic_palette)

    def fade_in_animation(self):
        """Add a smooth fade-in animation for the window."""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1000)  # 1 second
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.start()

    def add_intelligent_life_tab(self):
        """Tab for calculating the probability of intelligent life."""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Graph widget
        self.life_figure = Figure(facecolor="#2E3440")
        self.life_canvas = FigureCanvas(self.life_figure)
        self.life_canvas.setStyleSheet("background-color: #2E3440; border-radius: 10px;")
        layout.addWidget(self.life_canvas)

        # Parameters
        self.current_age = 13.8e9  # Current age of the universe
        self.stars_dying_age = 1e12  # Time when stars start dying

        # Slider for time selection (scaled down to fit within 32-bit integer range)
        self.time_slider = QSlider(Qt.Orientation.Horizontal)
        self.time_slider.setMinimum(0)
        self.time_slider.setMaximum(1000)  # Scaled range
        self.time_slider.setValue(int((self.current_age / self.stars_dying_age) * 1000))
        self.time_slider.valueChanged.connect(self.update_life_plot)
        self.time_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #4C566A;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #81A1C1;
                width: 20px;
                height: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
        """)
        layout.addWidget(QLabel("Select time after the Big Bang (years):"))
        layout.addWidget(self.time_slider)

        # Input field for time
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("Enter time in years...")
        self.time_input.setStyleSheet("""
            QLineEdit {
                background: #4C566A;
                color: #D8DEE9;
                border: 1px solid #81A1C1;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.time_input.returnPressed.connect(self.update_slider_from_input)
        layout.addWidget(self.time_input)

        # Update button
        self.update_button = QPushButton("Update Graph")
        self.update_button.setStyleSheet("""
            QPushButton {
                background: #81A1C1;
                color: #2E3440;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background: #88C0D0;
            }
        """)
        self.update_button.clicked.connect(self.update_life_plot)
        layout.addWidget(self.update_button)

        # Initial plot
        self.update_life_plot()

        # Add tab
        self.tabs.addTab(tab, "Intelligent Life Probability")

    def add_asteroid_collision_tab(self):
        """Tab for calculating the probability of an asteroid collision."""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Graph widget
        self.asteroid_figure = Figure(facecolor="#2E3440")
        self.asteroid_canvas = FigureCanvas(self.asteroid_figure)
        self.asteroid_canvas.setStyleSheet("background-color: #2E3440; border-radius: 10px;")
        layout.addWidget(self.asteroid_canvas)

        # Parameters
        self.asteroid_probability = 1e-8  # Base probability per year (example value)

        # Slider for asteroid probability
        self.asteroid_slider = QSlider(Qt.Orientation.Horizontal)
        self.asteroid_slider.setMinimum(0)
        self.asteroid_slider.setMaximum(100)
        self.asteroid_slider.setValue(int(self.asteroid_probability * 1e8))
        self.asteroid_slider.valueChanged.connect(self.update_asteroid_plot)
        self.asteroid_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #4C566A;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #81A1C1;
                width: 20px;
                height: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
        """)
        layout.addWidget(QLabel("Adjust asteroid collision probability (per year):"))
        layout.addWidget(self.asteroid_slider)

        # Input field for asteroid probability
        self.asteroid_input = QLineEdit()
        self.asteroid_input.setPlaceholderText("Enter probability (e.g., 1e-8)...")
        self.asteroid_input.setStyleSheet("""
            QLineEdit {
                background: #4C566A;
                color: #D8DEE9;
                border: 1px solid #81A1C1;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.asteroid_input.returnPressed.connect(self.update_asteroid_slider_from_input)
        layout.addWidget(self.asteroid_input)

        # Update button
        self.asteroid_update_button = QPushButton("Update Graph")
        self.asteroid_update_button.setStyleSheet("""
            QPushButton {
                background: #81A1C1;
                color: #2E3440;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background: #88C0D0;
            }
        """)
        self.asteroid_update_button.clicked.connect(self.update_asteroid_plot)
        layout.addWidget(self.asteroid_update_button)

        # Initial plot
        self.update_asteroid_plot()

        # Add tab
        self.tabs.addTab(tab, "Asteroid Collision Probability")

    def probability_of_intelligent_life(self, X):
        """Calculate the probability of intelligent life occurring X years after the Big Bang."""
        if X < 0:
            return 0.0
        elif X <= self.current_age:
            return X / self.current_age
        elif X <= self.stars_dying_age:
            return 1 - (X - self.current_age) / (self.stars_dying_age - self.current_age)
        else:
            return 0.0

    def update_slider_from_input(self):
        """Update the slider based on the input value."""
        try:
            time = float(self.time_input.text())
            # Scale the input value to fit the slider range
            scaled_time = (time / self.stars_dying_age) * 1000
            self.time_slider.setValue(int(scaled_time))
        except ValueError:
            print("Error: Please enter a valid number.")

    def update_life_plot(self):
        """Update the intelligent life probability plot."""
        self.life_figure.clear()

        # Get current time (scaled back to actual years)
        scaled_time = self.time_slider.value()
        time = (scaled_time / 1000) * self.stars_dying_age

        # Create plot
        ax = self.life_figure.add_subplot(111)
        x_values = [t for t in range(0, int(self.stars_dying_age * 1.2), int(1e9))]
        y_values = [self.probability_of_intelligent_life(t) for t in x_values]

        # Plot data
        ax.plot(x_values, y_values, label="Probability of Intelligent Life", color="#81A1C1")
        ax.axvline(x=time, color='r', linestyle='--', label=f"Current Time: {time:.1e} years")
        ax.set_xlabel("Time after the Big Bang (years)")
        ax.set_ylabel("Probability")
        ax.set_title("Probability of Intelligent Life in the Universe")
        ax.legend()
        ax.grid(True)
        ax.set_facecolor("#2E3440")
        ax.tick_params(colors="#D8DEE9")
        ax.xaxis.label.set_color("#D8DEE9")
        ax.yaxis.label.set_color("#D8DEE9")
        ax.title.set_color("#D8DEE9")

        # Update canvas
        self.life_canvas.draw()

    def update_asteroid_slider_from_input(self):
        """Update the asteroid slider based on the input value."""
        try:
            probability = float(self.asteroid_input.text())
            self.asteroid_slider.setValue(int(probability * 1e8))
        except ValueError:
            print("Error: Please enter a valid number.")

    def update_asteroid_plot(self):
        """Update the asteroid collision probability plot."""
        self.asteroid_figure.clear()

        # Get current probability
        probability = self.asteroid_slider.value() / 1e8

        # Create plot
        ax = self.asteroid_figure.add_subplot(111)
        years = [year for year in range(0, 1000000, 100000)]  # Up to 1 million years
        collision_probability = [1 - (1 - probability) ** year for year in years]

        # Plot data
        ax.plot(years, collision_probability, label="Cumulative Collision Probability", color="#81A1C1")
        ax.set_xlabel("Time (years)")
        ax.set_ylabel("Probability")
        ax.set_title("Probability of an Asteroid Collision with Earth")
        ax.legend()
        ax.grid(True)
        ax.set_facecolor("#2E3440")
        ax.tick_params(colors="#D8DEE9")
        ax.xaxis.label.set_color("#D8DEE9")
        ax.yaxis.label.set_color("#D8DEE9")
        ax.title.set_color("#D8DEE9")

        # Update canvas
        self.asteroid_canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Use Fusion style
    window = CosmicOdyssey()
    window.show()
    sys.exit(app.exec())