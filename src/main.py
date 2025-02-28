from camera.camera_stream import CameraStream
from hand_tracking.tracker import HandTracker
from cursor.cursor_control import CursorControl
from cursor.setting_manager import SettingManager
from thread.thread_manager import ThreadManager
from gui.gui import HandTrackingGUI
from PyQt6.QtWidgets import QApplication
import sys

def main():
  camera = CameraStream()
  tracker = HandTracker()
  settings = SettingManager()
  cursor = CursorControl(settings)
  thread_manager = ThreadManager()

  app = QApplication(sys.argv)
  gui = HandTrackingGUI(thread_manager, tracker, cursor, camera)
  gui.show()
  sys.exit(app.exec())

if __name__ == "__main__":
  main()