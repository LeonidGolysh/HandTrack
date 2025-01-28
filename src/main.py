from camera.camera_stream import CameraStream
from hand_tracking.tracker import HandTracker
from cursor.cursor_control import CursorControl
import cv2

def main():
  camera = CameraStream()
  tracker = HandTracker()
  cursor = CursorControl()

  try:
    while True:
      frame = camera.get_frame()
      if frame is None:
        print("Failed to get frame")
        break

      frame, results = tracker.process_frame(frame)

      if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
          if not cursor.is_calibrated:
            cursor.calibrate_vertical_range(hand_landmarks.landmark)

          if tracker.is_open_hand(hand_landmarks.landmark):
            cursor.move_cursor_with_hand(hand_landmarks.landmark)

          cursor.handle_pinch(tracker.is_pinch(hand_landmarks.landmark), hand_landmarks.landmark)

          if tracker.is_pinch(hand_landmarks.landmark) and not cursor.is_holding:
            cursor.click()

          if tracker.is_pinch_right(hand_landmarks.landmark):
            cursor.right_click()
          
          # if tracker.is_fist(hand_landmarks.landmark):
          #   cursor.scroll()

      camera.show_frame("Camera", frame)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  finally:
    camera.release()
    tracker.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
  main()