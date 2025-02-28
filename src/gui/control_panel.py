from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSlider
from PyQt6.QtCore import Qt

class ControlPanel(QWidget):
  def __init__(self, cursor):
    super().__init__()
    self.cursor = cursor

    self.start_button = QPushButton("Start")
    self.stop_button = QPushButton("Stop")

    self.scroll_speed_label = QLabel(f"Scroll speed: {self.cursor.scroll_speed}")
    self.scroll_speed_slider = QSlider(Qt.Orientation.Horizontal)
    self.scroll_speed_slider.setMinimum(10)
    self.scroll_speed_slider.setMaximum(500)
    self.scroll_speed_slider.setValue(self.cursor.scroll_speed)
    self.scroll_speed_slider.valueChanged.connect(self.update_scroll_speed)

    self.cursor_speed_label = QLabel(f"Cursor speed: {self.cursor.cursor_speed}")
    self.cursor_speed_slider = QSlider(Qt.Orientation.Horizontal)
    self.cursor_speed_slider.setMinimum(1)
    self.cursor_speed_slider.setMaximum(10)
    self.cursor_speed_slider.setValue(int(self.cursor.cursor_speed))
    self.cursor_speed_slider.valueChanged.connect(self.update_cursor_speed)

    button_layout = QHBoxLayout()
    button_layout.addWidget(self.start_button)
    button_layout.addWidget(self.stop_button)

    scroll_layout = QVBoxLayout()
    scroll_layout.addWidget(self.scroll_speed_label)
    scroll_layout.addWidget(self.scroll_speed_slider)
    scroll_layout.addWidget(self.cursor_speed_label)
    scroll_layout.addWidget(self.cursor_speed_slider)

    layout = QVBoxLayout()
    layout.addLayout(button_layout)
    layout.addLayout(scroll_layout)
    self.setLayout(layout)

  def update_scroll_speed(self, value):
    self.cursor.update_scroll_speed(value)
    self.scroll_speed_label.setText(f"Scroll speed: {value}")

  def update_cursor_speed(self, value):
    self.cursor.update_cursor_speed(float(value))
    self.cursor_speed_label.setText(f"Cursor speed: {value}")