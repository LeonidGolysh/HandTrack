import pyautogui
import time
import webbrowser

class CursorControl:
  def __init__(self):
    self.min_y = 0
    self.max_y = 1
    self.is_calibrated = False
    self.prev_x = 0
    self.prev_y = 0
    self.alpha = 0.5
    self.pinch_start_time = None
    self.is_holding = False       # Long hold flag
    self.direction_start_time = None      # To prevent multiple calls
    self.last_navigation = None
    self.is_easter_egg_detected = False

  def calibrate_vertical_range(self, landmarks):
    self.min_y = min(landmarks, key=lambda lm: lm.y).y
    self.max_y = max(landmarks, key=lambda lm: lm.y).y

    self.is_calibrated = True

  def move_cursor_with_hand(self, landmarks):
    if not self.is_calibrated:
        raise ValueError("CursorControl is not calibrated. Call `calibrate_vertical_range` first.")

    screen_width, screen_height = pyautogui.size()

    wrist = landmarks[0]

    normalized_y = (wrist.y - self.min_y) / (self.max_y - self.min_y)

    cursor_x = int((1 - wrist.x) * screen_width * 1.0)
    cursor_y = int(normalized_y * screen_height)

    # Motion smoothing
    smoothed_x = self.prev_x + (cursor_x - self.prev_x) * self.alpha
    smoothed_y = self.prev_y + (cursor_y - self.prev_y) * self.alpha

    # Limit cursor movement
    smoothed_x = max(1, min(smoothed_x, screen_width - 2))
    smoothed_y = max(1, min(smoothed_y, screen_height - 2))

    self.prev_x, self.prev_y = smoothed_x, smoothed_y

    # Move cursor to new screen coordinate
    pyautogui.moveTo(smoothed_x, smoothed_y)

  def click(self):
    pyautogui.click()

  def right_click(self):
    pyautogui.rightClick()

  def handle_pinch(self, is_pinch_active, landmarks):
    if is_pinch_active:
      if self.pinch_start_time is None:
        self.pinch_start_time = time.time()
        self.is_holding = False
      elif time.time() - self.pinch_start_time > 1:
        if not self.is_holding:
          print("Starting long press")
          pyautogui.mouseDown()
          self.is_holding = True

      self.move_cursor_with_hand(landmarks)
    else:
      if self.is_holding:
        print("Releasing long press")
        pyautogui.mouseUp()
        # self.is_holding = False

      self.pinch_start_time = None
      self.is_holding = False

  def handle_scroll(self, landmarks):
    wrist = landmarks[0]

    screen_height = pyautogui.size()[1]
    normalized_y = (wrist.y - self.min_y) / (self.max_y - self.min_y)

    if normalized_y < 0.5:
      pyautogui.scroll(100)
    else:
      pyautogui.scroll(-100)

  def handle_navigation(self, tracker, landmarks):
    if self.is_holding:
      return 

    direction = tracker.detect_index_finger_direction(landmarks)

    if direction == "left":
      if self.direction_start_time is None:
        self.direction_start_time = time.time()       # Start of motion recording
      elif time.time() - self.direction_start_time > 1 and self.last_navigation != "left":       # Direction confirmation after 1 seconds
        print("Go back")
        pyautogui.hotkey('alt', 'left')
        self.direction_start_time = None
        self.last_navigation = "left"
    
    elif direction == "right":
      if self.direction_start_time is None:
        self.direction_start_time = time.time()
        
      elif time.time() - self.direction_start_time > 1 and self.last_navigation != "right":
        print("Go forward")
        pyautogui.hotkey('alt', 'right')
        self.direction_start_time = None
        self.last_navigation = "right"
    else:
      self.direction_start_time = None
      self.last_navigation = None

  def handle_easter_egg(self, tracker, landmarks):
    if tracker.gesture_for_easter_egg(landmarks):
      if not self.is_easter_egg_detected:
        webbrowser.open("http://zenitbol.ru/_nw/171/43331998.jpg")
        self.is_easter_egg_detected = True
    else:
      self.is_easter_egg_detected = False