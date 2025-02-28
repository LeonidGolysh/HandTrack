from PyQt6.QtWidgets import QLabel, QFrame
from PyQt6.QtCore import Qt

class VideoWidget(QLabel):
  def __init__(self):
    super().__init__()
    self.setText("Video")
    self.setFrameShape(QFrame.Shape.Box)
    self.setAlignment(Qt.AlignmentFlag.AlignCenter)