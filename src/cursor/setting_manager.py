import json
import os

class SettingManager:
  CONFIG_FILE = "config.json"

  def __init__(self):
    self.settings = self.load_settings()

  def load_settings(self):
    if os.path.exists(self.CONFIG_FILE):
      with open(self.CONFIG_FILE, "r") as f:
        return json.load(f)
    return {}
  
  def save_settings(self):
    with open(self.CONFIG_FILE, "w") as f:
      json.dump(self.settings, f)

  def get_setting(self, key, default=None):
    return self.settings.get(key, default)

  def set_setting(self, key, value):
    self.settings[key] = value
    self.save_settings()

  def get_scroll_speed(self):
    return self.get_setting("scroll_speed", 100)
  
  def set_scroll_speed(self, speed):
    self.set_setting("scroll_speed", speed)

  def get_cursor_speed(self):
    return self.get_setting("cursor_speed", 1.0)
  
  def set_cursor_speed(self, speed):
    self.set_setting("cursor_speed", speed)