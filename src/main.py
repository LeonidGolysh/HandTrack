from camera.camera_stream import CameraStream
from hand_tracking.tracker import HandTracker
from cursor.cursor_control import CursorControl
from thread.thread_manager import ThreadManager
import cv2

def process_hand_tracking(frame, tracker, cursor):
  frame, results = tracker.process_frame(frame)

  if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
      if not cursor.is_calibrated:
        cursor.calibrate_vertical_range(hand_landmarks.landmark)

      if tracker.is_open_hand(hand_landmarks.landmark):
        cursor.move_cursor_with_hand(hand_landmarks.landmark)

      cursor.handle_easter_egg(tracker, hand_landmarks.landmark)
      cursor.handle_navigation(tracker, hand_landmarks.landmark)
      cursor.handle_pinch(tracker.is_pinch(hand_landmarks.landmark), hand_landmarks.landmark)

      if tracker.is_pinch(hand_landmarks.landmark) and not cursor.is_holding:
        cursor.click()

      if tracker.is_pinch_right(hand_landmarks.landmark):
        cursor.right_click()
      
      if tracker.is_fist(hand_landmarks.landmark):
        cursor.handle_scroll(hand_landmarks.landmark)

  return frame

def main():
  camera = CameraStream()
  tracker = HandTracker()
  cursor = CursorControl()
  thread_manager = ThreadManager()

  thread_manager.start_camera_thread(camera)

  try:
    while True:
      frame = thread_manager.get_latest_frame()
      if frame is None:
        continue
      
      future = thread_manager.processed_frame_async(process_hand_tracking, frame, tracker, cursor)
      processed_frame = future.result()

      camera.show_frame("Camera", processed_frame)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  finally:
    thread_manager.stop()
    camera.release()
    tracker.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
  main()