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
pygame.init()
pygame.display.set_caption('Mouse position to keyboard input')
screen_height = 600
screen_width = 800
lines_width = 1
lines_color = (0,0,0)
font_color = (0,0,0)
background_color = (255,255,255)
background_color_blocked = (178,34,34)
background_color_hover = (50,205,50)
font = pygame.font.Font('freesansbold.ttf', 32) 
key_to_unlock = pygame.K_p
mapping = np.array(
    [
        [ ['q','z'], ['z'] ,  ['d','z'] ],
        [ ['q'], [] , ['d'] ],
        [ ['q','s'], ['s'] , ['d','s'] ]
    ]
)

case_width = (screen_width/3)+1
case_height = screen_height/3

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


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

        # Mouse positioning
        (x_mouse,y_mouse) = pygame.mouse.get_pos()
        mapping_col = int(x_mouse//(screen_width/3))
        mapping_line = int(y_mouse//(screen_height/3))

        # GUI
        pygame.draw.rect(screen, background_color, pygame.Rect(0, 0, screen_width, screen_height))

        #hover effect
        x_pos = mapping_col * (screen_width/3)
        y_pos = mapping_line * (screen_height/3)
        pygame.draw.rect(screen, background_color_hover, pygame.Rect(x_pos, y_pos, case_width, case_height))

        pygame.draw.line(screen, lines_color, (screen_width/3, 0), (screen_width/3, screen_height), lines_width)
        pygame.draw.line(screen, lines_color, (screen_width/3*2, 0), (screen_width/3*2, screen_height), lines_width)
        pygame.draw.line(screen, lines_color, (0, screen_height/3), (screen_width, screen_height/3), lines_width)
        pygame.draw.line(screen, lines_color, (0, screen_height/3*2), (screen_width, screen_height/3*2), lines_width)

        # display keys
        for line_index, line in enumerate(mapping):
            for col_index, keys in enumerate(line):
                text = font.render('+'.join(keys), True, font_color, background_color) 
                textRect = text.get_rect()  
                x = ((screen_width/3)*(col_index+1)) - (screen_width/3)/2
                y = ((screen_height/3)*(line_index+1)) - (screen_height/3)/2
                textRect.center = (x,y) 
                screen.blit(text, textRect) 

        if pressed_keys:
            for pressed_key in pressed_keys:
                pyautogui.keyDown(pressed_key)
        if pressed_keys != mapping[mapping_line][mapping_col]:
            if pressed_keys:
                for pressed_key in pressed_keys:
                    pyautogui.keyUp(pressed_key)
            pressed_keys = mapping[mapping_line][mapping_col]
    else:
        pygame.draw.rect(screen, background_color_blocked, pygame.Rect(0, 0, screen_width, screen_height)) 
        text = font.render('press "p" to lock/unlock', True, font_color, None) 
        textRect = text.get_rect()  
        x = screen_width/2
        y = screen_height/2
        textRect.center = (x,y) 
        screen.blit(text, textRect)       

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == key_to_unlock:
                launched = not launched

    pygame.display.update()
