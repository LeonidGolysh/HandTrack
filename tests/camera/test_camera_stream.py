import unittest
import cv2
import numpy as np
from src.camera.camera_stream import CameraStream
from unittest.mock import MagicMock, patch

class TestCameraStream(unittest.TestCase):

  @patch('src.camera.camera_stream.cv2.VideoCapture')
  def test_get_frame(self, mock_video_capture):
    mock_cap = MagicMock()
    mock_cap.isOpened.return_value = True
    mock_cap.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))

    mock_video_capture.return_value = mock_cap

    camera_stream = CameraStream()
    frame = camera_stream.get_frame()

    self.assertIsNotNone(frame)
    self.assertIsInstance(frame, np.ndarray)
    self.assertEqual(frame.shape, (480, 640, 3))

    camera_stream.release()
    mock_cap.release.assert_called_once()

if __name__ == "__main__":
  unittest.main()