import threading
from concurrent.futures import ThreadPoolExecutor

class ThreadManager:
  def __init__(self):
    self.lock = threading.Lock()
    self.executor = ThreadPoolExecutor(max_workers=2)
    self.frame = None
    self.running = True

  def start_camera_thread(self, camera):
    def capture_frames():
      while self.running:
        temp_frame = camera.get_frame()
        if temp_frame is None:
          print("Failed to get frame")
          break
        with self.lock:
          self.frame = temp_frame

    threading.Thread(target=capture_frames, daemon=True).start()

  def get_latest_frame(self):
    with self.lock:
      return self.frame.copy() if self.frame is not None else None
    
  def processed_frame_async(self, func, *args):
    return self.executor.submit(func, *args)
  
  def stop(self):
    self.running = False
    self.executor.shutdown()