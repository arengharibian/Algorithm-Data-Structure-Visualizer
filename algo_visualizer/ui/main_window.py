# ui/main_window.py
import random
from typing import Optional, Generator, List, Tuple

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from algorithms import ALGORITHMS
from ui.visualizer_canvas import VisualizerCanvas

State = Tuple[List[int], Optional[int], Optional[int]]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Algorithm Visualizer – Sorting")
        self.resize(900, 600)

        # Core state
        self.current_data: List[int] = []
        self.current_generator: Optional[Generator[State, None, None]] = None
        self.running: bool = False

        # Timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.step_algorithm)

        # Build UI
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)

        # Controls
        control_layout = QHBoxLayout()

        # Algorithm selector
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(list(ALGORITHMS.keys()))
        control_layout.addWidget(QLabel("Algorithm:"))
        control_layout.addWidget(self.algorithm_combo)

        # Array size
        control_layout.addWidget(QLabel("Size:"))
        self.size_spin = QSpinBox()
        self.size_spin.setRange(5, 200)
        self.size_spin.setValue(50)
        control_layout.addWidget(self.size_spin)

        # Speed slider (interval ms)
        control_layout.addWidget(QLabel("Speed:"))
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 100)  # 1 (fast) to 100 (slow)
        self.speed_slider.setValue(30)
        self.speed_slider.valueChanged.connect(self.update_timer_interval)
        control_layout.addWidget(self.speed_slider)

        # Buttons
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_data)
        control_layout.addWidget(self.generate_button)

        self.start_button = QPushButton("▶ Play")
        self.start_button.clicked.connect(self.start_animation)
        control_layout.addWidget(self.start_button)

        self.pause_button = QPushButton("⏸ Pause")
        self.pause_button.clicked.connect(self.pause_animation)
        control_layout.addWidget(self.pause_button)

        self.step_button = QPushButton("Step")
        self.step_button.clicked.connect(self.step_algorithm)
        control_layout.addWidget(self.step_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_animation)
        control_layout.addWidget(self.reset_button)

        control_layout.addStretch()

        main_layout.addLayout(control_layout)

        # Canvas
        self.canvas = VisualizerCanvas()
        main_layout.addWidget(self.canvas, stretch=1)

        # Info label at bottom
        self.info_label = QLabel("Ready.")
        main_layout.addWidget(self.info_label)

        # Initial setup
        self.update_timer_interval()
        self.generate_data()

    # ----------------- Core logic -----------------

    def update_timer_interval(self):
        # Map slider (1–100) to interval (10–500 ms)
        slider_value = self.speed_slider.value()
        interval = 10 + int((slider_value / 100) * 490)
        self.timer.setInterval(interval)

    def generate_data(self):
        size = self.size_spin.value()
        # random array values between 10 and 100
        self.current_data = [random.randint(10, 100) for _ in range(size)]
        self.current_generator = None
        self.running = False
        self.timer.stop()
        self.canvas.set_state(self.current_data, None, None)
        self.info_label.setText(f"Generated new array of size {size}.")

    def ensure_generator(self):
        if self.current_generator is None:
            algo_name = self.algorithm_combo.currentText()
            algo_func = ALGORITHMS[algo_name]
            self.current_generator = algo_func(self.current_data)
            self.info_label.setText(f"Running {algo_name}...")

    def start_animation(self):
        self.ensure_generator()
        self.running = True
        self.timer.start()

    def pause_animation(self):
        self.running = False
        self.timer.stop()
        self.info_label.setText("Paused.")

    def reset_animation(self):
        # Just regenerate current array shape with new random values
        if not self.current_data:
            self.generate_data()
            return
        size = len(self.current_data)
        self.current_data = [random.randint(10, 100) for _ in range(size)]
        self.current_generator = None
        self.running = False
        self.timer.stop()
        self.canvas.set_state(self.current_data, None, None)
        self.info_label.setText("Reset with new random values.")

    def step_algorithm(self):
        if self.current_generator is None:
            self.ensure_generator()

        if self.current_generator is None:
            return

        try:
            data, i, j = next(self.current_generator)
            self.current_data = data
            self.canvas.set_state(data, i, j)
        except StopIteration:
            self.timer.stop()
            self.running = False
            self.current_generator = None
            self.canvas.set_state(self.current_data, None, None)
            self.info_label.setText("Sorting complete.")
