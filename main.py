import pyautogui
import time
import keyboard
import random
from pynput.mouse import Button, Controller
import pygetwindow as gw
import tkinter as tk
from tkinter import simpledialog
import colorama
from colorama import Fore, Style

mouse = Controller()
time.sleep(0.5)

colorama.init()

print(Fore.GREEN + Style.BRIGHT + """
┌──────────────────────┐
│   BLUM autoclicker   │
│       by xolop       │
└──────────────────────┘
""" + Style.RESET_ALL)

def click(x, y):
    mouse.position = (x, y + random.randint(1, 3))
    mouse.press(Button.left)
    mouse.release(Button.left)

def choose_window_gui():
    root = tk.Tk()
    root.withdraw()

    windows = gw.getAllTitles()
    if not windows:
        return None

    choice = simpledialog.askstring("Выбор окна Telegram", "Введите номер окна:\n" + "\n".join(f"{i}: {window}" for i, window in enumerate(windows)))

    if choice is None or not choice.isdigit():
        return None

    choice = int(choice)
    if 0 <= choice < len(windows):
        return windows[choice]
    else:
        return None

window_name = "TelegramDesktop"
check = gw.getWindowsWithTitle(window_name)

if not check:
    print(f"\nОкно {window_name} не найдено!\nПожалуйста, выберите другое окно.")
    window_name = choose_window_gui()

if not window_name or not gw.getWindowsWithTitle(window_name):
    print("\nНе удалось найти указанное окно!\nЗапустите Telegram, после чего перезапустите бота!")
else:
    print(f"\nОкно {window_name} найдено\nНажмите 'S' для старта.")

if window_name:
    telegram_window = gw.getWindowsWithTitle(window_name)[0]
else:
    telegram_window = None

paused = True
last_check_time = time.time()

while True:
    if keyboard.is_pressed('S'):
        paused = not paused
        if paused:
            print('Пауза')
        else:
            print('Работаю')
            print(f"Для паузы нажми 'S'")
        time.sleep(0.2)

    if paused:
        continue

    if telegram_window:
        window_rect = (
            telegram_window.left, telegram_window.top, telegram_window.width, telegram_window.height
        )

        try:
            telegram_window.activate()
        except:
            telegram_window.minimize()
            telegram_window.restore()

        scrn = pyautogui.screenshot(region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))

        width, height = scrn.size
        pixel_found = False
        if pixel_found == True:
            break

        for x in range(0, width, 20):
            for y in range(0, height, 20):
                r, g, b = scrn.getpixel((x, y))
                if (b in range(0, 125)) and (r in range(102, 220)) and (g in range(200, 255)):
                    screen_x = window_rect[0] + x + 3
                    screen_y = window_rect[1] + y + 5
                    click(screen_x, screen_y)
                    time.sleep(0.01)
                    pixel_found = True
                    break
    else:
        print("\nНе удалось найти указанное окно!\nЗапустите Telegram, после чего перезапустите бота!")
        break

print('Стоп')
