import tkinter as tk
import threading
import pyautogui
import time 
import requests
import ctypes

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
SW_HIDE = 0
hWnd = kernel32.GetConsoleWindow()
user32.ShowWindow(hWnd, SW_HIDE)


class MouseLockerApp:
    def __init__(self, root):

        self.usetime = 3600
        self.headers = {
            'Authorization': 'Bearer ' + '9lkUbDS0zxrkbJX8VixsaNzE7qGSnH9TqmxwRH8eN39'    
        }
        data = requests.post('https://notify-api.line.me/api/notify', headers=self.headers, data={'message':'    目前無人使用' }) 
        self.root = root
        self.root.title("Mouse Locker")
        
        self.locked = False

        self.instructions_label = tk.Label(root, text="Enter your name to unlock the mouse:")
        self.instructions_label.pack()

        self.name_entry = tk.Entry(root)
        self.name_entry.pack()
        self.name_entry.focus_set()  # Set focus to the entry widget

        self.welcome_label = tk.Label(root, text="")
        self.welcome_label.pack()

        self.lock_mouse()
        self.name_entry.bind("<Return>", self.check_name)
        

    def lock_mouse(self):
        self.locked = True
        threading.Thread(target=self.move_mouse_to_center).start()

    def unlock_mouse(self):
        self.locked = False
        threading.Thread(target=self.lock_mouse_after_delay).start()

    def lock_mouse_after_delay(self):
        
        time.sleep(self.usetime)  
        self.locked = True
        self.lock_mouse()

    def move_mouse_to_center(self):
        while self.locked:
            screen_width, screen_height = pyautogui.size()
            pyautogui.moveTo(screen_width // 2, screen_height // 2)

    def check_name(self, event):
        self.lock_mouse()
        name = self.name_entry.get().strip()
        print(name)
        if name:
            self.welcome_label.config(text="Welcome! You can now use the mouse.")
            self.locked = False
            self.unlock_mouse()
            name="    "+name+" 使用中,使用時間："+str(self.usetime) + "秒"
            requests.post('https://notify-api.line.me/api/notify', headers=self.headers, data={'message':name }) 
        else:
            self.welcome_label.config(text="Please enter a valid name.")


if __name__ == "__main__":
    root = tk.Tk()
    app = MouseLockerApp(root)
    while True:
        root.mainloop()
        root.destroy()
        root = tk.Tk()
        app = MouseLockerApp(root)
