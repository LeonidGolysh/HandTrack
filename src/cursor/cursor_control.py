import pyautogui

class CursorControl:
  def __init__(self):
    self.min_y = 0
    self.max_y = 1
    self.is_calibrated = False
    self.prev_x = 0
    self.prev_y = 0
    self.alpha = 0.5

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
