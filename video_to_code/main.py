import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import shutil
from PIL import Image, ImageTk
import cv2


class VideoProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Processing App")

        self.label = tk.Label(root, text="Выберите видео для обработки:")
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.browse_button = tk.Button(root, text="Обзор", command=self.browse_video)
        self.browse_button.grid(row=1, column=0, pady=10)

        self.process_button = tk.Button(root, text="Начать обработку", command=self.process_video)
        self.process_button.grid(row=1, column=1, pady=10)

        self.status_label = tk.Label(root, text="")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=10)

        self.video_path = None

        self.video_label = tk.Label(root)
        self.video_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.text_display = tk.Text(root, height=10, width=50)
        self.text_display.grid(row=4, column=0, columnspan=2, pady=10)

        self.check_results_button = tk.Button(root, text="Проверить результат", command=self.display_output_results)
        self.check_results_button.grid(row=5, column=0, columnspan=2, pady=10)

    def browse_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
        if file_path:
            # Копирование видеофайла в папку 1_video_to_24fps и переименование в "video.mp4"
            destination_path = os.path.join(current_directory, "1_video_to_24fps", "video.mp4")
            shutil.copy(file_path, destination_path)
            self.video_path = destination_path
            self.status_label.config(text=f"Выбрано видео: {os.path.basename(destination_path)}")

    def delete_frames(self):
        frames_folder = os.path.join(current_directory, "2_video24_to_image/images")
        if os.path.exists(frames_folder):
            shutil.rmtree(frames_folder)
            os.makedirs(frames_folder)
    
    def delete_reconstructed_images(self):
        images_folder = os.path.join(current_directory, "x_text_to_image/reconstructed_images")
        if os.path.exists(images_folder):
            shutil.rmtree(images_folder)
            os.makedirs(images_folder)


    def process_video(self):
        if self.video_path:
            # Удаление всех кадров перед обработкой
            self.delete_frames()
            self.delete_reconstructed_images()

            # Первый этап: изменение частоты кадров
            subprocess.run(["python", os.path.join(current_directory, "1_video_to_24fps/video24.py"), self.video_path])
            self.status_label.config(text="1 этап завершен")

            # Второй этап: разделение видео на кадры
            subprocess.run(["python", os.path.join(current_directory, "2_video24_to_image/video2image.py")])
            self.status_label.config(text="2 этап завершен")

            # Третий этап: анализ кадров и запись цветов в текстовый документ
            subprocess.run(["python", os.path.join(current_directory, "3_image_to_text/image2text.py")])
            self.status_label.config(text="3 этап завершен")

            # Четвертый этап: создание изображений из текстового файла
            subprocess.run(["python", os.path.join(current_directory, "x_text_to_image/text2image.py")])
            self.status_label.config(text="4 этап завершен")

            # Пятый этап: создание видео из изображений
            subprocess.run(["python", os.path.join(current_directory, "x_image_to_video/image2video.py")])
            self.status_label.config(text="5 этап завершен")

            # Отображение кнопки "Проверить результат"
            self.check_results_button.grid(row=5, column=0, columnspan=2, pady=10)

    def display_output_results(self):
        output_file_path = os.path.join(current_directory, "3_image_to_text/output.txt")
        with open(output_file_path, 'r') as f:
            output_data = f.read()
            self.text_display.insert(tk.END, output_data)

        # Загрузка видео в плеер после нажатия "Проверить результат"
        self.load_video_to_player()

    def show_frame(self):
        if hasattr(self, 'cap'):
            ret, frame = self.cap.read()

            if ret:
                # Преобразование изображения OpenCV в формат PhotoImage
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image=image)

                # Обновление изображения на Label
                self.video_label.config(image=photo)
                self.video_label.image = photo

                # Рекурсивный вызов для следующего кадра
                self.root.after(10, self.show_frame)
            else:
                self.cap.release()
                self.status_label.config(text="Воспроизведение завершено")

    def load_video_to_player(self):
        video_path = os.path.join(current_directory, "x_image_to_video", "output_video.mp4")
        self.cap = cv2.VideoCapture(video_path)

        # Воспроизведение видео
        self.show_frame()

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))

    root = tk.Tk()
    app = VideoProcessingApp(root)
    root.mainloop()
