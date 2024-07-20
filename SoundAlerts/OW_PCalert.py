import json
import os
import sys
import keyboard
import pyautogui
from time import sleep
import pyautogui
from PIL import Image
import ctypes
import pygame

target_hex = "B3601F"

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Function to check if a color is within an acceptable range of the target color
def is_color_similar(color1, color2, tolerance=30):
    return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(color1, color2))

# Function to monitor a pixel for a range of similar colors
def monitor_pixel(x, y, tolerance=30):
    global target_hex
    target_color = tuple(int(target_hex[i:i+2], 16) for i in (0, 2, 4))
    while True:
        screenshot = pyautogui.screenshot(region=(x, y, 1, 1))
        rgb_im = screenshot.convert('RGB')
        pixel_color = rgb_im.getpixel((0, 0))
        if is_color_similar(pixel_color, target_color, tolerance):
            # print("Similar color detected at the specified pixel.")
            play_sound(resource_path('airhorn.mp3'))
            break
        sleep(0.1)

# Function to check and update the run status
def check_first_run():
    settings_file = 'settings.json'
    if not os.path.exists(settings_file):
        # Default settings for first run
        settings = {'first_run': True}
        with open(settings_file, 'w') as file:
            json.dump(settings, file)

    with open(settings_file, 'r') as file:
        settings = json.load(file)

    return settings

# Function to update the JSON file after the first run
def update_settings(new_settings):
    with open('settings.json', 'w') as file:
        json.dump(new_settings, file)

def notifier(x, y):
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    monitor_pixel(x, y)

# Main function to handle first run and pixel coordinates
def main():
    settings = check_first_run()
    if settings.get('first_run'):
        print("First time setup: Welcome to Overwatch Found Game Notifier (PC alerts version)")
        sleep(4)
        print("Thank you for installing!")
        sleep(3)
        print("\nCreated by Cammy (noLimit#11169) github.com/jjcamber")
        sleep(3)
        input("\nPress enter to continue to setup")
        print("\n\nTo begin, if you have not already, please pin Overwatch to your taskbar and move it to a location on your taskbar that will remain consistent.")
        sleep(5)
        input("\nPress enter to continue once this is done")
        print("\n\nPlease move your mouse cursor over the corner of the pinned Overwatch application on your taskbar.")
        sleep(5)
        print("\nMake sure it is not placed over the filled in portion of the icon, rather, the unfilled space to the side of it.")
        sleep(6)
        print("\nOnce your cursor is properly placed, press the spacebar key to save the pixel coordinates.")
        while True:
            if keyboard.is_pressed('space'):
                x, y = pyautogui.position()
                settings['first_run'] = False
                settings['pixel_coordinates'] = {'x': x, 'y': y}
                update_settings(settings)
                print(f"\n\nCoordinates saved: {x}, {y}")
                sleep(3)
                print("\nThe window will close soon. We recommend placing a shortcut on your desktop to the exe or directly running the exe to begin using.")
                sleep(6)
                break
    else:
        x = settings['pixel_coordinates']['x']
        y = settings['pixel_coordinates']['y']
        notifier(x, y)

if __name__ == "__main__":
    main()
