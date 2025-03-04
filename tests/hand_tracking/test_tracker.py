import unittest
import numpy as np
import cv2
from unittest.mock import MagicMock, patch
from src.hand_tracking.tracker import HandTracker

class TestHandTracker(unittest.TestCase):
  @patch('src.hand_tracking.tracker.mp_hands.Hands')
  @patch('src.hand_tracking.tracker.mp_drawing.draw_landmarks')
  def test_process_frame(self, mock_draw_landmarks, mock_hands):
    mock_result = MagicMock()
    mock_result.multi_hand_landmarks = [MagicMock()]

    mock_hands.return_value.process.return_value = mock_result

    tracker = HandTracker()

    fake_frame = np.zeros((480, 640, 3), dtype=np.uint8)

    process_frame, results = tracker.process_frame(fake_frame)

    self.assertIsNotNone(process_frame)
    self.assertEqual(results, mock_result)
    mock_draw_landmarks.assert_called()

if __name__ == '__main__':
  unittest.main()