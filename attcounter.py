import tkinter as tk
from tkinter import font, colorchooser, simpledialog
import keyboard
import json
import os

class AttemptCounter:
    def __init__(self, root, save_file='settings.json'):
        self.root = root
        self.root.title("Attempt Counter")
        self.root.geometry("300x150")
        
        self.save_file = save_file
        self.load_settings()
        
        self.custom_font = font.Font(family=self.font_name, size=self.font_size)
        
        self.label = tk.Label(root, text=f"Attempts: {self.attempts}", font=self.custom_font, fg=self.text_color, bg=self.bg_color)
        self.label.pack(expand=True, fill=tk.BOTH)
        
        self.create_menu()
        
        self.update_hotkeys()
    
    def update_hotkeys(self):
        # Unhook existing hotkeys
        if hasattr(self, 'hotkey_id'):
            keyboard.unhook_key(self.hotkey)
        if hasattr(self, 'reset_key_id'):
            keyboard.unhook_key(self.reset_key)
        
        # Set new hotkeys
        keyboard.on_press_key(self.hotkey, lambda _: self.increment_attempts())
        keyboard.on_press_key(self.reset_key, lambda _: self.reset_attempts())
    
    def increment_attempts(self):
        self.attempts += 1
        self.label.config(text=f"Attempts: {self.attempts}")
        self.save_settings()
    
    def reset_attempts(self):
        self.attempts = 0
        self.label.config(text=f"Attempts: {self.attempts}")
        self.save_settings()

    def set_attempts(self):
        new_attempts = simpledialog.askinteger("Set Attempts", "Enter new number of attempts:", initialvalue=self.attempts)
        if new_attempts is not None:
            self.attempts = new_attempts
            self.label.config(text=f"Attempts: {self.attempts}")
            self.save_settings()
    
    def save_settings(self):
        settings = {
            'attempts': self.attempts,
            'hotkey': self.hotkey,
            'reset_key': self.reset_key,
            'font_name': self.font_name,
            'font_size': self.font_size,
            'text_color': self.text_color,
            'bg_color': self.bg_color
        }
        with open(self.save_file, 'w') as f:
            json.dump(settings, f)
    
    def load_settings(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as f:
                settings = json.load(f)
                self.attempts = settings.get('attempts', 0)
                self.hotkey = settings.get('hotkey', 'space')
                self.reset_key = settings.get('reset_key', 'r')
                self.font_name = settings.get('font_name', 'Helvetica')
                self.font_size = settings.get('font_size', 24)
                self.text_color = settings.get('text_color', 'blue')
                self.bg_color = settings.get('bg_color', 'lightgrey')
        else:
            self.attempts = 0
            self.hotkey = 'space'
            self.reset_key = 'r'
            self.font_name = 'Helvetica'
            self.font_size = 24
            self.text_color = 'blue'
            self.bg_color = 'lightgrey'
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        
        settings_menu.add_command(label="Set Hotkey", command=self.set_hotkey)
        settings_menu.add_command(label="Set Reset Key", command=self.set_reset_key)
        settings_menu.add_command(label="Set Font", command=self.set_font)
        settings_menu.add_command(label="Set Font Size", command=self.set_font_size)
        settings_menu.add_command(label="Set Text Color", command=self.set_text_color)
        settings_menu.add_command(label="Set Background Color", command=self.set_bg_color)
        settings_menu.add_command(label="Set Attempts", command=self.set_attempts)
    
    def set_hotkey(self):
        new_hotkey = simpledialog.askstring("Set Hotkey", "Enter new hotkey:", initialvalue=self.hotkey)
        if new_hotkey:
            self.hotkey = new_hotkey
            self.update_hotkeys()
            self.save_settings()
    
    def set_reset_key(self):
        new_reset_key = simpledialog.askstring("Set Reset Key", "Enter new reset key:", initialvalue=self.reset_key)
        if new_reset_key:
            self.reset_key = new_reset_key
            self.update_hotkeys()
            self.save_settings()
    
    def set_font(self):
        new_font_name = simpledialog.askstring("Set Font", "Enter new font name:", initialvalue=self.font_name)
        if new_font_name:
            self.font_name = new_font_name
            self.custom_font.config(family=self.font_name)
            self.label.config(font=self.custom_font)
            self.save_settings()
    
    def set_font_size(self):
        new_font_size = simpledialog.askinteger("Set Font Size", "Enter new font size:", initialvalue=self.font_size)
        if new_font_size:
            self.font_size = new_font_size
            self.custom_font.config(size=self.font_size)
            self.label.config(font=self.custom_font)
            self.save_settings()
    
    def set_text_color(self):
        new_text_color = colorchooser.askcolor(title="Choose text color", initialcolor=self.text_color)[1]
        if new_text_color:
            self.text_color = new_text_color
            self.label.config(fg=self.text_color)
            self.save_settings()
    
    def set_bg_color(self):
        new_bg_color = colorchooser.askcolor(title="Choose background color", initialcolor=self.bg_color)[1]
        if new_bg_color:
            self.bg_color = new_bg_color
            self.label.config(bg=self.bg_color)
            self.root.config(bg=self.bg_color)
            self.save_settings()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = AttemptCounter(root)
    app.run()
