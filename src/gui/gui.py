from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QTimer
from concurrent.futures import Future
from thread.thread_manager import ThreadManager
from camera.camera_stream import CameraStream
from hand_tracking.tracker import HandTracker
from cursor.cursor_control import CursorControl
from gui.video_widget import VideoWidget
from gui.control_panel import ControlPanel
import cv2
import numpy as np

class HandTrackingGUI(QWidget):
  def __init__(self, thread_manager, tracker, cursor, camera):
    super().__init__()

    self.thread_manager = thread_manager
    self.tracker = tracker
    self.cursor = cursor
    self.camera = camera

    self.setWindowTitle("Hand Tracking Interface")
    self.setGeometry(100, 100, 800, 600)

    self.video_widget = VideoWidget()
    self.control_panel = ControlPanel(self.cursor)

    layout = QVBoxLayout()
    layout.addWidget(self.video_widget)
    layout.addWidget(self.control_panel)
    self.setLayout(layout)

    self.control_panel.start_button.clicked.connect(self.start_tracking)
    self.control_panel.stop_button.clicked.connect(self.stop_tracking)

    self.timer = QTimer()
    self.timer.timeout.connect(self.update_frame)

    self.future: Future = None

  def start_tracking(self):
    self.thread_manager.start_camera_thread(self.camera)
    self.timer.start(20)

  def stop_tracking(self):
    self.timer.stop()
    self.thread_manager.stop()

  def process_hand_tracking(self, frame):
    frame, results = self.tracker.process_frame(frame)

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        if not self.cursor.is_calibrated:
          self.cursor.calibrate_vertical_range(hand_landmarks.landmark)

        if self.tracker.is_open_hand(hand_landmarks.landmark):
          self.cursor.move_cursor_with_hand(hand_landmarks.landmark)

        self.cursor.handle_easter_egg(self.tracker, hand_landmarks.landmark)
        self.cursor.handle_navigation(self.tracker, hand_landmarks.landmark)
        self.cursor.handle_pinch(self.tracker.is_pinch(hand_landmarks.landmark), hand_landmarks.landmark)

        if self.tracker.is_pinch(hand_landmarks.landmark) and not self.cursor.is_holding:
          self.cursor.click()

        if self.tracker.is_pinch_right(hand_landmarks.landmark):
          self.cursor.right_click()
        
        if self.tracker.is_fist(hand_landmarks.landmark):
          self.cursor.handle_scroll(hand_landmarks.landmark)

    return frame

  def update_frame(self):
    if self.future and not self.future.done():
      return

    frame = self.thread_manager.get_latest_frame()
    if frame is None:
      return

    self.future = self.thread_manager.processed_frame_async(self.process_hand_tracking, frame)

    processed_frame = self.future.result()
    self.display_frame(processed_frame)

  def display_frame(self, frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    height, width, channel = frame.shape
    bytes_per_line = channel * width
    q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
    pixmap = QPixmap.fromImage(q_img)

    self.video_widget.setPixmap(pixmap)

  def closeEvent(self, event):
    self.stop_tracking()
    self.camera.release()
    self.tracker.release()
    cv2.destroyAllWindows()
    event.accept()