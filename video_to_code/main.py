import shutil
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QRadioButton, QButtonGroup
from PyQt5 import QtCore
import subprocess

class VideoProcessingApp(QMainWindow):
    def __init__(self):
        super(VideoProcessingApp, self).__init__()

        self.setWindowTitle("Video Processing App")

        # Создание главного макета
        main_layout = QVBoxLayout()

        # Основное окно
        main_widget = QWidget(self)

        layout = QVBoxLayout(main_widget)

        self.label = QLabel("Выберите видео для обработки:")
        layout.addWidget(self.label)

        self.browse_button = QPushButton("Обзор", clicked=self.browse_video)
        layout.addWidget(self.browse_button)

        self.processing_options_group = QButtonGroup(self)
        self.show_result_button = QRadioButton("Показать результат")
        self.hide_result_button = QRadioButton("Не показывать результат")
        self.processing_options_group.addButton(self.show_result_button)
        self.processing_options_group.addButton(self.hide_result_button)
        self.show_result_button.setChecked(True)
        layout.addWidget(self.show_result_button)
        layout.addWidget(self.hide_result_button)

        self.process_button = QPushButton("Начать обработку", clicked=self.process_video)
        layout.addWidget(self.process_button)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        main_layout.addWidget(main_widget)

        self.setCentralWidget(main_widget)

        # Инициализация переменной для папки вывода
        self.output_folder_for_second_stage = "2_video24_to_image\images"

    def browse_video(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Выберите видео", "", "Video files (*.mp4 *.avi)")
        if file_path:
            self.set_video_path(file_path)
            self.status_label.setText(f"Выбрано видео: {os.path.basename(file_path)}")

    def set_video_path(self, video_path):
        self.video_path_for_second_stage = video_path

    def delete_frames(self):
        # Удаляем папку с кадрами и создаем новую
        frames_folder = os.path.join(current_directory, self.output_folder_for_second_stage)
        if os.path.exists(frames_folder):
            shutil.rmtree(frames_folder)
        os.makedirs(frames_folder)

    def process_video(self):
        if hasattr(self, 'video_path_for_second_stage'):
            self.delete_frames()

            # Запускаем внешние процессы
            subprocess.run(["python", os.path.join(current_directory, "2_video24_to_image/video2image.py"),
                            self.video_path_for_second_stage, self.output_folder_for_second_stage])
            self.status_label.setText("2 этап завершен")

            subprocess.run(["python", os.path.join(current_directory, "3_image_to_text/image2text.py")])
            self.status_label.setText("3 этап завершен")

            if self.show_result_button.isChecked():
                subprocess.run(["python", os.path.join(current_directory, "x_text_to_image/text2image.py")])
                self.status_label.setText("4 этап завершен")

                subprocess.run(["python", os.path.join(current_directory, "x_image_to_video/image2video.py")])
                self.status_label.setText("5 этап завершен")

# Пример использования
if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))

    app = QApplication(sys.argv)
    main_window = VideoProcessingApp()
    main_window.show()

    sys.exit(app.exec_())
