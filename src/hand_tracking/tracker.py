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

        # self.recognize_gestures(hand_landmarks)

    return frame, results
  
  def recognize_gestures(self, hand_landmarks):
    if self.is_open_hand(hand_landmarks.landmark):
      print("Open hand")

    if self.is_pinch(hand_landmarks.landmark):
      print("Click")

    if self.is_fist(hand_landmarks.landmark):
      print("Closed hand")

    if self.is_custom_gesture(hand_landmarks.landmark):
      print("Test")

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

    return distance < 0.05

  def is_fist(self, landmarks):
    tips = [4, 8, 12, 16, 20]
    base_joints = [1, 5, 9, 13, 17]
    closed_fingers = 0
    for tip, base_joint in zip(tips, base_joints):
      if landmarks[tip].y > landmarks[base_joint].y:   # Fingertip below the joint
        closed_fingers += 1

    return closed_fingers == 5
  
  def is_custom_gesture(self, landmarks):
    open_fingers = 0
    closed_fingers = 0

    if landmarks[4].y < landmarks[1].y:
      open_fingers += 1
    else:
      closed_fingers += 1

    if landmarks[8].y > landmarks[5].y:
      open_fingers += 1
    else:
      closed_fingers += 1

    if landmarks[12].y > landmarks[9].y:
      open_fingers += 1
    else:
      closed_fingers += 1

    if landmarks[16].y > landmarks[13].y:
      open_fingers += 1
    else:
      closed_fingers += 1

    if landmarks[20].y > landmarks[17].y:
      open_fingers += 1
    else:
      closed_fingers += 1

    return open_fingers == 2 and closed_fingers == 3

  def release(self):
    self.hands.close()