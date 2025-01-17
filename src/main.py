from camera.camera_stream import CameraStream
from hand_tracking.tracker import HandTracker
import cv2

def main():
  camera = CameraStream()
  tracker = HandTracker()

  try:
    while True:
      frame = camera.get_frame()
      if frame is None:
        print("Failed to get frame")
        break

      frame, results = tracker.process_frame(frame)

      camera.show_frame("Camera", frame)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  finally:
    camera.release()
    tracker.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
  main()