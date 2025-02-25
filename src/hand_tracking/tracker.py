# from cursor.cursor_control import CursorControl
import mediapipe as mp
import math
import cv2

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

class HandTracker:
  def __init__(self):
    self.hands = mp_hands.Hands(
      model_complexity=1,
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5
    )

  def process_frame(self, frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = self.hands.process(frame_rgb)

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
          frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
        )

    return frame, results

  def is_open_hand(self, landmarks):
    tips = [4, 8, 12, 16, 20]
    open_fingers = 0

    for tip in tips:
      if landmarks[tip].y < landmarks[tip - 2].y:   # Fingertip above the joint
        open_fingers += 1

    return open_fingers == 5
  
  def is_pinch(self, landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]

    distance = math.sqrt(
      (thumb_tip.x - index_tip.x) ** 2 +
      (thumb_tip.y - index_tip.y) ** 2 +
      (thumb_tip.z - index_tip.z) ** 2
    )

    return distance < 0.04
  
  def is_pinch_right(self, landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[12]

    distance = math.sqrt(
      (thumb_tip.x - index_tip.x) ** 2 +
      (thumb_tip.y - index_tip.y) ** 2 +
      (thumb_tip.z - index_tip.z) ** 2
    )

    return distance < 0.03
  
  def is_bunch(self, landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]

    avg_x = (thumb_tip.x + index_tip.x + middle_tip.x + ring_tip.x + pinky_tip.x) / 5
    avg_y = (thumb_tip.y + index_tip.y + middle_tip.y + ring_tip.y + pinky_tip.y) / 5
    avg_z = (thumb_tip.z + index_tip.z + middle_tip.z + ring_tip.z + pinky_tip.z) / 5

    max_distance = 0
    for tip in [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]:
      distance = math.sqrt(
        (tip.x - avg_x) ** 2 +
        (tip.y - avg_y) ** 2 +
        (tip.z - avg_z) ** 2
      )
      max_distance = max(max_distance, distance)

      return max_distance < 0.03

  def is_fist(self, landmarks):
    tips = [8, 12, 16, 20]
    base_joints = [5, 9, 13, 17]
    closed_fingers = 0
    for tip, base_joint in zip(tips, base_joints):
      if landmarks[tip].y > landmarks[base_joint].y:   # Fingertip below the joint
        closed_fingers += 1

    return closed_fingers == 4
  
  def detect_index_finger_direction(self, landmarks):
    base_x = landmarks[5].x     # Base of the finger
    tip_x = landmarks[8].x      # Fingertip

    if tip_x < base_x - 0.05:
      return "left"
    elif tip_x > base_x + 0.05:
      return "right"
    return None

  def gesture_for_easter_egg(self, landmarks):
    return (
        landmarks[12].y < landmarks[10].y and
        landmarks[8].y > landmarks[6].y and
        landmarks[16].y > landmarks[14].y and
        landmarks[20].y > landmarks[18].y
    )

  def release(self):
    self.hands.close()