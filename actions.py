import pyautogui
import os
import time

last_action_time = 0
COOLDOWN = 1.5  # seconds

def can_trigger():
    global last_action_time
    if time.time() - last_action_time > COOLDOWN:
        last_action_time = time.time()
        return True
    return False

def play_pause():
    if can_trigger():
        pyautogui.press("playpause")

def next_track():
    if can_trigger():
        pyautogui.press("nexttrack")

def prev_track():
    if can_trigger():
        pyautogui.press("prevtrack")

def volume_mute():
    if can_trigger():
        pyautogui.press("volumemute")

def lock_screen():
    if can_trigger():
        pyautogui.hotkey("win", "l")

def close_app():
    if can_trigger():
        pyautogui.hotkey("alt", "f4")

def shutdown_pc():
    if can_trigger():
        os.system("shutdown /s /t 1")
