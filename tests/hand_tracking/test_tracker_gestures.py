import unittest
from unittest.mock import MagicMock
from src.hand_tracking.tracker import HandTracker

class TestHandTrackerGestures(unittest.TestCase):
  def setUp(self):
    self.tracker = HandTracker()

  def mock_landmark(self, x, y, z=0):
    landmark = MagicMock()
    landmark.x = x
    landmark.y = y
    landmark.z = z
    return landmark
  
  def test_is_open_true(self):
    # Simulate an open palm: all fingertips are above the previous joints
    landmarks = [self.mock_landmark(0,0) for _ in range(21)]
    # Set 'y' so that fingertips (tip) is higher (smaller un 'y') than tip - 2
    landmarks[4].y = 0.1
    landmarks[2].y = 0.2
    landmarks[8].y = 0.1
    landmarks[6].y = 0.2
    landmarks[12].y = 0.1
    landmarks[10].y = 0.2
    landmarks[16].y = 0.1
    landmarks[14].y = 0.2
    landmarks[20].y = 0.1
    landmarks[18].y = 0.2

    result = self.tracker.is_open_hand(landmarks)
    self.assertTrue(result)

  def test_is_open_hand_false(self):
    landmarks = [self.mock_landmark(0,0) for _ in range(21)]
    # Put a least one finger bent
    landmarks[4].y = 0.3
    landmarks[2].y = 0.2

    result = self.tracker.is_open_hand(landmarks)
    self.assertFalse(result)

  def test_is_pinch_true(self):
    landmarks = [self.mock_landmark(0,0) for _ in range(21)]
    landmarks[4] = self.mock_landmark(0.1, 0.1)
    landmarks[8] = self.mock_landmark(0.12, 0.12)   # Distance < 0.04

    result = self.tracker.is_pinch(landmarks)
    self.assertTrue(result)

  def test_is_pinch_false(self):
    landmarks = [self.mock_landmark(0,0) for _ in range(21)]
    landmarks[4] = self.mock_landmark(0.1, 0.1)
    landmarks[8] = self.mock_landmark(0.5, 0.5)   # Distance > 0.04

    result = self.tracker.is_pinch(landmarks)
    self.assertFalse(result)

  def test_is_right_pinch_true(self):
    landmarks = [self.mock_landmark(0,0) for _ in range(21)]
    landmarks[4] = self.mock_landmark(0.1, 0.1)
    landmarks[12] = self.mock_landmark(0.11, 0.11)    # Distance < 0.03

    result = self.tracker.is_pinch_right(landmarks)
    self.assertTrue(result)

  def test_is_right_pinch_false(self):
    landmarks = [self.mock_landmark(0,0) for _ in range(21)]
    landmarks[4] = self.mock_landmark(0.1, 0.1)
    landmarks[12] = self.mock_landmark(0.5, 0.5)

    result = self.tracker.is_pinch_right(landmarks)
    self.assertFalse(result)

  def test_is_bunch_true(self):
    landmarks = [self.mock_landmark(0,0) for _ in range(21)]
    # All fingers are close to each other (small spread)
    landmarks[4] = self.mock_landmark(0.1, 0.1)
    landmarks[8] = self.mock_landmark(0.11, 0.1)
    landmarks[12] = self.mock_landmark(0.1, 0.11)
    landmarks[16] = self.mock_landmark(0.11, 0.11)
    landmarks[20] = self.mock_landmark(0.1, 0.1)

    result = self.tracker.is_bunch(landmarks)
    self.assertTrue(result)

  def test_is_bunch_false(self):
    landmarks = [self.mock_landmark(0,0) for _ in range(21)]
    # All fingers are far from each other (wide spread)
    landmarks[4] = self.mock_landmark(0.1, 0.1)
    landmarks[8] = self.mock_landmark(0.5, 0.5)
    landmarks[12] = self.mock_landmark(0.9, 0.9)
    landmarks[16] = self.mock_landmark(0.5, 0.1)
    landmarks[20] = self.mock_landmark(0.1, 0.5)

    result = self.tracker.is_bunch(landmarks)
    self.assertFalse(result)

  def test_is_fist_true(self):
    landmarks = [self.mock_landmark(0, 0) for _ in range(21)]
    # All fingers are bent: fingertip below base_joint
    landmarks[8].y = 0.5
    landmarks[5].y = 0.4
    landmarks[12].y = 0.6
    landmarks[9].y = 0.5
    landmarks[16].y = 0.7
    landmarks[13].y = 0.6
    landmarks[20].y = 0.8
    landmarks[17].y = 0.7

    result = self.tracker.is_fist(landmarks)
    self.assertTrue(result)

  def test_is_fist_false(self):
    landmarks = [self.mock_landmark(0, 0) for _ in range(21)]
    # At least one finger is open (fingertip above base_joint)
    landmarks[8].y = 0.3
    landmarks[5].y = 0.4
    landmarks[12].y = 0.6
    landmarks[9].y = 0.5
    landmarks[16].y = 0.7
    landmarks[13].y = 0.6
    landmarks[20].y = 0.8
    landmarks[17].y = 0.7

    result = self.tracker.is_fist(landmarks)
    self.assertFalse(result)

  def test_detect_index_finger_direction_left(self):
    landmarks = [self.mock_landmark(0, 0) for _ in range(21)]
    landmarks[5] = self.mock_landmark(0.5, 0.5)
    landmarks[8] = self.mock_landmark(0.4, 0.5)

    result = self.tracker.detect_index_finger_direction(landmarks)
    self.assertEqual(result, "left")

  def test_detect_index_finger_direction_right(self):
    landmarks = [self.mock_landmark(0, 0) for _ in range(21)]
    landmarks[5] = self.mock_landmark(0.5, 0.5)
    landmarks[8] = self.mock_landmark(0.6, 0.5)

    result = self.tracker.detect_index_finger_direction(landmarks)
    self.assertEqual(result, "right")

  def test_detect_index_finger_direction_none(self):
    landmarks = [self.mock_landmark(0, 0) for _ in range(21)]
    landmarks[5] = self.mock_landmark(0.5, 0.5)
    landmarks[8] = self.mock_landmark(0.52, 0.5)

    result = self.tracker.detect_index_finger_direction(landmarks)
    self.assertIsNone(result)

  def test_gesture_for_easter_egg_true(self):
    landmarks = [self.mock_landmark(0, 0) for _ in range(21)]
    landmarks = [self.mock_landmark(0, 0) for _ in range(21)]
    landmarks[12].y = 0.4
    landmarks[10].y = 0.5
    landmarks[8].y = 0.6
    landmarks[6].y = 0.5
    landmarks[16].y = 0.6
    landmarks[14].y = 0.5
    landmarks[20].y = 0.6
    landmarks[18].y = 0.5

    result = self.tracker.gesture_for_easter_egg(landmarks)
    self.assertTrue(result)

  def test_gesture_for_easter_egg_false(self):
    landmarks = [self.mock_landmark(0, 0) for _ in range(21)]
    landmarks[12].y = 0.5
    landmarks[10].y = 0.4
    landmarks[8].y = 0.4
    landmarks[6].y = 0.5
    landmarks[16].y = 0.4
    landmarks[14].y = 0.5
    landmarks[20].y = 0.4
    landmarks[18].y = 0.5

    result = self.tracker.gesture_for_easter_egg(landmarks)
    self.assertFalse(result)

if __name__ == '__main__':
  unittest.main()