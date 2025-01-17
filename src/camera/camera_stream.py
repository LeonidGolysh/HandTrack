import cv2

class CameraStream:
  def __init__(self, camera_index=0):
    self.cap = cv2.VideoCapture(camera_index)

  def get_frame(self):
    if self.cap.isOpened():
      ret, frame = self.cap.read()
      if ret:
        return frame
    return None
  
  def release(self):
    self.cap.release()

  @staticmethod
  def show_frame(window_name, frame):
    cv2.imshow(window_name, frame)