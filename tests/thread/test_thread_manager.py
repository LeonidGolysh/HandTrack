import unittest
import numpy as np
import time
from unittest.mock import MagicMock
from src.thread.thread_manager import ThreadManager

class TestThreadManager(unittest.TestCase):
  def setUp(self):
    self.thread_manager = ThreadManager()

  def tearDown(self):
    self.thread_manager.stop()

  def test_start_camera_thread(self):
    mock_camera = MagicMock()
    mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    mock_camera.get_frame.side_effect = [mock_frame] * 5 + [None]

    self.thread_manager.start_camera_thread(mock_camera)

    time.sleep(0.2)     # Time for the thread to download and capture the frame

    frame = self.thread_manager.get_latest_frame()
    self.assertIsNotNone(frame)
    self.assertTrue((frame == mock_frame).all())

  def test_processing_frame_async(self):
    def mock_processing(frame):
      return frame.sum()
    
    mock_frame = np.ones((10, 10, 3), dtype=np.uint8)
    future = self.thread_manager.processed_frame_async(mock_processing, mock_frame)
    result = future.result(timeout=1)

    self.assertEqual(result, 10 * 10 * 3)

  def test_stop(self):
    self.thread_manager.stop()
    self.assertFalse(self.thread_manager.running)

if __name__ == '__main__':
  unittest.main()