import tkinter as tk
import pygame
from tkinter import filedialog, messagebox, simpledialog
from pygame import mixer
from exceptions import AudioPlayerError, FileLoadError, PlaybackError, StopPlaybackError


class AudioPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Player App")
        self.root.geometry("400x300")


        pygame.mixer.init()
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Открыть", command=self.load_audio)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menu.add_cascade(label="Файл", menu=file_menu)

        settings_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Настройки", menu=settings_menu)

    def create_widgets(self):
        self.play_button = tk.Button(self.root, text="▶️ Воспроизвести", command=self.play_audio, state=tk.DISABLED)
        self.play_button.pack(pady=20)

        self.stop_button = tk.Button(self.root, text="⏹️ Остановить", command=self.stop_audio, state=tk.DISABLED)
        self.stop_button.pack(pady=20)

    def load_audio(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")]
            )
            if not file_path:
                raise FileLoadError("Файл не был выбран.")
            self.current_file = file_path
            self.play_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            messagebox.showinfo("Файл загружен", f"Файл успешно загружен:\n{file_path}")
        except FileLoadError as e:
            messagebox.showwarning("Ошибка загрузки файла", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def play_audio(self):
        try:
            if not self.current_file:
                raise PlaybackError("Файл для воспроизведения не был загружен.")
            pygame.mixer.music.load(self.current_file)
            pygame.mixer.music.play()
        except PlaybackError as e:
            messagebox.showwarning("Ошибка воспроизведения", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось воспроизвести файл: {e}")

    def stop_audio(self):
        try:
            if not pygame.mixer.music.get_busy():
                raise StopPlaybackError("Нет активного воспроизведения для остановки.")
            pygame.mixer.music.stop()
        except StopPlaybackError as e:
            messagebox.showwarning("Ошибка остановки", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось остановить воспроизведение: {e}")