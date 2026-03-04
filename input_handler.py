import pyautogui
import random
import pydirectinput
from randomizer import random_click_offset, random_delay

#pyautogui has a built-in delay -> we need to disable that one
pyautogui.PAUSE = 0

class InputHandler:
    def __init__(self):
        #fail safe -> move mouse to corner of screen to stop the bot
        pyautogui.FAILSAFE = True

    def click(self, position):
        #unpack position into x and y
        x, y = position
        #apply random offset
        x, y = random_click_offset(x, y)
        #move mouse to position and click
        pyautogui.moveTo(x, y, duration=self._mouse_duration())
        random_delay()
        pyautogui.click()

    def shift_click(self, position):
        x, y = position
        x, y = random_click_offset(x, y)
        pyautogui.moveTo(x, y, duration=self._mouse_duration())
        random_delay()
        pyautogui.click()

    def hold_shift(self):
        pydirectinput.keyDown("shift")

    def release_shift(self):
        pydirectinput.keyUp("shift")

    def _mouse_duration(self):
        #how long the mouse takes to move to the target
        return random.gauss(0.2, 0.05)