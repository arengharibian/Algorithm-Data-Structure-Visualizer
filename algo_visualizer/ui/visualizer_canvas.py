# ui/visualizer_canvas.py
from typing import List, Optional

from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget


class VisualizerCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data: List[int] = []
        self._active_a: Optional[int] = None
        self._active_b: Optional[int] = None

    def set_state(self, data: List[int], active_a: Optional[int], active_b: Optional[int]):
        self._data = data
        self._active_a = active_a
        self._active_b = active_b
        self.update()

    def clear(self):
        self._data = []
        self._active_a = None
        self._active_b = None
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self._data:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)

        width = self.width()
        height = self.height()

        n = len(self._data)
        if n == 0:
            return

        max_val = max(self._data)
        bar_width = max(1, width // n)

        for i, value in enumerate(self._data):
            bar_height = int((value / max_val) * (height * 0.9))
            x = i * bar_width
            y = height - bar_height

            rect = QRect(x, y, bar_width - 1, bar_height)

            # Color bars differently if they are active
            if i == self._active_a or i == self._active_b:
                painter.setBrush(Qt.red)
            else:
                painter.setBrush(Qt.darkCyan)

            painter.setPen(Qt.black)
            painter.drawRect(rect)

        painter.end()
