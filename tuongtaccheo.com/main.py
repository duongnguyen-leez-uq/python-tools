import numpy as np
import pyautogui
import cv2
import keyboard
import mouse
from time import sleep

def take_a_screenshot():
    image = pyautogui.screenshot()
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def find_location(image, template):
    h, w = template.shape[:-1]
    threshold = 0.8

    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

    loc = np.where(res >= threshold)
    loc = [(pt[0], pt[1]) for pt in zip(*loc[::-1])]  # Switch collumns and rows
    loc = [(int(pt[0] + w/2), int(pt[1] + h/2)) for pt in loc]  # centre

    return loc

def move_to_image_on_screen(template , index = 0):
    screen = take_a_screenshot()
    loc = find_location(screen, template)

    if len(loc) == 0:
        return False

    first_loc = loc[index]
    print(first_loc)
    mouse.move(first_loc[0], first_loc[1], duration=1)

    return True


image_earn_money_button = cv2.imread('images/earn-money-button.png')
image_follow_button = cv2.imread('images/follow-button.png')
image_following_button = cv2.imread('images/following-button.png')
image_open_follow_task = cv2.imread('images/open-follow-task.png')
image_reset_button = cv2.imread('images/reset-button.png')
image_unfollow_button = cv2.imread('images/unfollow-button.png')

keyboard.press_and_release('alt+tab')
# keyboard.press_and_release('ctrl+tab')
# keyboard.press_and_release('ctrl+w')

print('ok')
sleep(2)
while True:
    if len(find_location(take_a_screenshot(), image_open_follow_task)) == 0:
        sleep(1)
        move_to_image_on_screen(image_reset_button)
        mouse.click('left')
        sleep(8)
        continue

    if move_to_image_on_screen(image_open_follow_task):
        mouse.click('left')

        sleep(6)
        if move_to_image_on_screen(image_follow_button):
            mouse.click('left')
            sleep(1.8)
            keyboard.press_and_release('ctrl+tab')

            sleep(0.5)
            move_to_image_on_screen(image_earn_money_button)
            mouse.click('left')
            sleep(2)
            keyboard.press_and_release('ctrl+tab')
            sleep(0.5)
            move_to_image_on_screen(image_following_button, index=-1)
            sleep(0.5)
            move_to_image_on_screen(image_unfollow_button)
            mouse.click('left')
            sleep(2)
            keyboard.press_and_release('ctrl+w')
            sleep(1)
        else:
            keyboard.press_and_release('ctrl+w')
            sleep(3)
            move_to_image_on_screen(image_earn_money_button)
            mouse.click('left')
            sleep(2)