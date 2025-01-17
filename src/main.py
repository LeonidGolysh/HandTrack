from camera.camera_stream import CameraStream
import cv2

def main():
  camera = CameraStream()

  try:
    while True:
      frame = camera.get_frame()
      if frame is None:
        print("Failed to get frame")
        break
        
      camera.show_frame("Camera", frame)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  finally:
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
  main()