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

        self.stop_button = None
        self.pause_button = None
        self.play_button = None
        self.progress_scale = None
        self.file_label = None
        self.current_file = None
        self.is_paused = False  # Флаг для отслеживания состояния паузы
        self.paused_position = 0  # Сохранённая позиция при паузе (в миллисекундах)

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Открыть", command=self.load_audio)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

        settings_menu = tk.Menu(menu, tearoff=0)
        settings_menu.add_command(label="Настроить размер окна", command=self.resize_window)
        menu.add_cascade(label="Настройки", menu=settings_menu)

    def create_widgets(self):
        # Метка для отображения текущего файла
        self.file_label = tk.Label(self.root, text="Файл не выбран", wraplength=380, justify="center")
        self.file_label.pack(pady=10)

        # Ползунок для прогресса
        self.progress_scale = tk.Scale(
            self.root,
            from_=0,
            to=100,
            orient="horizontal",  # Горизонтальный ползунок
            length=350,  # Ширина ползунка
            state="disabled",  # Отключён по умолчанию
        )
        self.progress_scale.pack(pady=10)

        # Кнопка воспроизведения
        self.play_button = tk.Button(self.root, text="▶️ Воспроизвести", command=self.play_audio, state=tk.DISABLED)
        self.play_button.pack(pady=10)

        # Кнопка паузы
        self.pause_button = tk.Button(self.root, text="⏸️ Пауза", command=self.pause_audio, state=tk.DISABLED)
        self.pause_button.pack(pady=10)

        # Кнопка остановки
        self.stop_button = tk.Button(self.root, text="⏹️ Остановить", command=self.stop_audio, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

    def load_audio(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")]
            )
            if not file_path:
                raise FileLoadError("Файл не был выбран.")
            self.current_file = file_path

            # Включаем кнопки
            self.play_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.NORMAL)

            # Обновляем метку файла
            self.file_label.config(text=f"Текущий файл: {file_path}")

            # Устанавливаем длину трека
            duration = self.get_audio_duration()
            if duration > 0:
                self.progress_scale.config(state="normal", from_=0, to=duration // 1000)  # Максимум в секундах

            messagebox.showinfo("Файл загружен", f"Файл успешно загружен:\n{file_path}")
        except FileLoadError as e:
            messagebox.showwarning("Ошибка загрузки файла", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def get_audio_duration(self):
        try:
            if self.current_file:
                sound = pygame.mixer.Sound(self.current_file)
                return int(sound.get_length() * 1000)  # Длительность в миллисекундах
            return 0
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить длительность аудио: {e}")
            return 0

    def play_audio(self):
        try:
            if not self.current_file:
                raise PlaybackError("Файл для воспроизведения не был загружен.")

            if self.is_paused:  # Если трек на паузе
                pygame.mixer.music.unpause()  # Снимаем паузу
                self.is_paused = False
            elif not pygame.mixer.music.get_busy():  # Если музыка не играет
                pygame.mixer.music.load(self.current_file)
                pygame.mixer.music.play(loops=0, start=self.paused_position / 1000)  # С учетом паузы
                self.paused_position = 0  # Сбрасываем паузу

            self.update_progress()  # Запускаем обновление прогресса
        except PlaybackError as e:
            messagebox.showwarning("Ошибка воспроизведения", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось воспроизвести файл: {e}")

    def pause_audio(self):
        try:
            if pygame.mixer.music.get_busy() and not self.is_paused:  # Если музыка играет
                self.paused_position = pygame.mixer.music.get_pos()  # Сохраняем текущую позицию
                pygame.mixer.music.pause()  # Ставим на паузу
                self.is_paused = True  # Устанавливаем флаг паузы
            elif self.is_paused:  # Если музыка уже на паузе
                messagebox.showinfo("Пауза", "Музыка уже на паузе.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось поставить на паузу: {e}")

    def stop_audio(self):
        try:
            if not pygame.mixer.music.get_busy():
                raise StopPlaybackError("Нет активного воспроизведения для остановки.")
            pygame.mixer.music.stop()
            self.is_paused = False
            self.paused_position = 0
            self.progress_scale.set(0)  # Сбрасываем прогресс
        except StopPlaybackError as e:
            messagebox.showwarning("Ошибка остановки", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось остановить воспроизведение: {e}")

    def update_progress(self):
        if pygame.mixer.music.get_busy():  # Если музыка играет
            current_position = pygame.mixer.music.get_pos() // 1000  # Позиция в секундах
            self.progress_scale.set(current_position)  # Устанавливаем положение ползунка
            self.root.after(500, self.update_progress)  # Обновляем каждые 500 мс

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