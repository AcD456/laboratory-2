import tkinter as tk
import pygame
from tkinter import filedialog, messagebox, simpledialog
from pygame import mixer
from exceptions import FileLoadError, PlaybackError, StopPlaybackError

# Основной класс приложения
class AudioPlayerApp:
    def __init__(self, root):


        self.root = root
        self.root.title("Audio Player")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.iconbitmap("icon.ico")
        pygame.mixer.init()

        self.file_label = None
        self.current_file = None
        self.stop_button = None
        self.play_button = None
        self.pause_button = None
        self.is_paused = False  # Флаг для отслеживания состояния паузы
        self.paused_position = 0  # Сохранённая позиция при паузе (в миллисекундах)

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu = menu)

        file_menu = tk.Menu(menu, tearoff = 0)
        menu.add_cascade(label = "Файл", menu = file_menu)
        file_menu.add_command(label = "Открыть", command = self.load_audio)
        file_menu.add_separator()
        file_menu.add_command(label = "Выход", command = self.root.quit)

        settings_menu = tk.Menu(menu, tearoff = 0)
        settings_menu.add_command(label = "Настроить размер окна", command = self.resize_window)
        menu.add_cascade(label = "Настройки", menu = settings_menu)

    def create_widgets(self):
        self.file_label = tk.Label(self.root, text="Файл не выбран", wraplength=380, justify="center")
        self.file_label.pack(pady=10)

        self.play_button = tk.Button(self.root, text = "▶️ Воспроизвести", command = self.play_audio, state = tk.DISABLED)
        self.play_button.pack(pady = 10)

        self.pause_button = tk.Button(self.root, text = "⏸️ Пауза", command = self.pause_audio, state = tk.DISABLED)
        self.pause_button.pack(pady = 10)

        self.stop_button = tk.Button(self.root, text = "⏹️ Остановить", command = self.stop_audio, state = tk.DISABLED)
        self.stop_button.pack(pady = 10)

    def load_audio(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes = [("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")]
            )
            if not file_path:
                raise FileLoadError("Файл не был выбран.")
            self.current_file = file_path

            file_name = file_path.split("/")[-1]
            self.file_label.config(text=f"Текущий файл: {file_name}")
            #unlock widgets
            self.play_button.config(state = tk.NORMAL)
            self.stop_button.config(state = tk.NORMAL)
            self.pause_button.config(state = tk.NORMAL)
            messagebox.showinfo("Файл загружен", f"Файл успешно загружен:\n{file_path}")
        except FileLoadError as e:
            messagebox.showwarning("Ошибка загрузки файла", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def play_audio(self):
        try:
            if not self.current_file:
                raise PlaybackError("Файл для воспроизведения не был загружен.")
            # Загружаем и начинаем воспроизведение
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                messagebox.showinfo("Воспроизведение", "Воспроизведение продолжено.")
            else:
                # Загружаем и начинаем воспроизведение с начала или сохранённой позиции
                pygame.mixer.music.load(self.current_file)
                pygame.mixer.music.play(loops = 0, start = self.paused_position / 1000)  # Позиция в секундах
                self.paused_position = 0

        except PlaybackError as e:
            messagebox.showwarning("Ошибка воспроизведения", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось воспроизвести файл: {e}")

    def pause_audio(self):
        try:
            if pygame.mixer.music.get_busy():  # Проверяем, воспроизводится ли музыка
                if not self.is_paused:
                    self.paused_position = pygame.mixer.music.get_pos()  # Сохраняем текущую позицию в миллисекундах
                    pygame.mixer.music.pause()  # Ставим на паузу
                    self.is_paused = True  # Устанавливаем флаг паузы
                else:
                    raise StopPlaybackError("Нет активного воспроизведения для паузы.")
            else:
                raise StopPlaybackError("Нет активного воспроизведения для паузы.")
        except StopPlaybackError as e:
            messagebox.showwarning("Ошибка паузы", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось поставить на паузу: {e}")

    def stop_audio(self):
        try:
            if not pygame.mixer.music.get_busy():
                raise StopPlaybackError("Нет активного воспроизведения для остановки.")
            pygame.mixer.music.stop()
            self.is_paused = False  # Сбрасываем флаг паузы
            self.paused_position = 0  # Сброс позиции
        except StopPlaybackError as e:
            messagebox.showwarning("Ошибка остановки", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось остановить воспроизведение: {e}")

    def resize_window(self):
        try:
            new_width = tk.simpledialog.askinteger("Настройка размера", "Введите ширину окна:", minvalue = 200, maxvalue = 800)
            new_height = tk.simpledialog.askinteger("Настройка размера", "Введите высоту окна:", minvalue = 200, maxvalue = 600)
            if new_width and new_height:
                self.root.geometry(f"{new_width}x{new_height}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось изменить размер окна: {e}")

    def on_closing(self):
        try:
            pygame.mixer.quit()
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при закрытии приложения: {e}")