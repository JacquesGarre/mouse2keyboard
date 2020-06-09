import pygame
import win32api
import win32con
import win32gui
import numpy as np
from pygame.locals import *
import time
import os
import sys
import pyautogui

# Config
screen_height = 600
screen_width = 800
lines_width = 1
lines_color = (0,0,0)
background_color = (255,255,255)
refresh_rate = 0.0005
mapping = np.array(
    [
        [ ['q','z'], ['z'] ,  ['d','z'] ],
        [ ['q'], [] , ['d'] ],
        [ ['q','s'], ['s'] , ['d','s'] ]
    ]
)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()
pygame.display.set_caption('Mouse position to keyboard input')
screen = pygame.display.set_mode((screen_width, screen_height))
done = False

transparent = (255, 0, 128)
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparent), 0, win32con.LWA_COLORKEY)
pressed_keys = []
launched = False

while not done:
    if launched:
        if pressed_keys:
            for pressed_key in pressed_keys:
                pyautogui.keyDown(pressed_key)
        (x_mouse,y_mouse) = pygame.mouse.get_pos()
        mapping_col = int(x_mouse//(screen_width/3))
        mapping_line = int(y_mouse//(screen_height/3))
        if pressed_keys != mapping[mapping_line][mapping_col]:
            if pressed_keys:
                for pressed_key in pressed_keys:
                    pyautogui.keyUp(pressed_key)
            pressed_keys = mapping[mapping_line][mapping_col]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                launched = not launched
                print(launched)

    screen.fill(transparent) 


    pygame.draw.rect(screen, background_color, pygame.Rect(0, 0, screen_width, screen_height))
    pygame.draw.line(screen, lines_color, (screen_width/3, 0), (screen_width/3, screen_height), lines_width)
    pygame.draw.line(screen, lines_color, (screen_width/3*2, 0), (screen_width/3*2, screen_height), lines_width)
    pygame.draw.line(screen, lines_color, (0, screen_height/3), (screen_width, screen_height/3), lines_width)
    pygame.draw.line(screen, lines_color, (0, screen_height/3*2), (screen_width, screen_height/3*2), lines_width)
    pygame.display.update()
    time.sleep(refresh_rate)
