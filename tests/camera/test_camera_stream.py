import unittest
import cv2
import numpy as np
from src.camera.camera_stream import CameraStream

class TestCameraStream(unittest.TestCase):
  def setUp(self):
    self.camera = CameraStream()

  def tearDown(self):
    self.camera.release()

  def test_camera_initialization(self):
    self.assertIsInstance(self.camera.cap, cv2.VideoCapture)

  def test_get_frame(self):
    frame = self.camera.get_frame()
    self.assertTrue(
      frame is None or isinstance(frame, (np.ndarray, list, tuple))
      )

  def test_release_camera(self):
    self.camera.release()
    self.assertFalse(self.camera.cap.isOpened())

if __name__ == "__main__":
  unittest.main()