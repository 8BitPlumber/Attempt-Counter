import tkinter as tk
from tkinter import font
import keyboard
import json
import os

class AttemptCounter:
    def __init__(self, root, hotkey='shift', reset_key='r', font_name='Arial', font_size=20, text_color='black', bg_color='white', save_file='attempts.json'):
        self.hotkey = hotkey
        self.reset_key = reset_key
        self.font_name = font_name
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.save_file = save_file

        self.root = root
        self.root.title("Attempt Counter")
        self.root.geometry("300x150")
        self.root.configure(bg=self.bg_color)  # Set background color of the root window
        
        self.custom_font = font.Font(family=self.font_name, size=self.font_size)
        
        self.label = tk.Label(root, text="Attempts: 0", font=self.custom_font, fg=self.text_color, bg=self.bg_color)
        self.label.pack(expand=True)
        
        self.load_attempts()
        
        keyboard.on_press_key(self.hotkey, lambda _: self.increment_attempts())
        keyboard.on_press_key(self.reset_key, lambda _: self.reset_attempts())
    
    def increment_attempts(self):
        self.attempts += 1
        self.label.config(text=f"Attempts: {self.attempts}")
        self.save_attempts()
    
    def reset_attempts(self):
        self.attempts = 0
        self.label.config(text=f"Attempts: {self.attempts}")
        self.save_attempts()
    
    def save_attempts(self):
        with open(self.save_file, 'w') as f:
            json.dump({'attempts': self.attempts}, f)
    
    def load_attempts(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as f:
                data = json.load(f)
                self.attempts = data.get('attempts', 0)
                self.label.config(text=f"Attempts: {self.attempts}")
        else:
            self.attempts = 0
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = AttemptCounter(root, hotkey='shift', reset_key='r', font_name='Helvetica', font_size=24, text_color='white', bg_color='black')
    app.run()
