import numpy as np
import cv2
import os

def create_images(input_file, output_folder):
    # Получаем текущий путь к скрипту
    script_path = os.path.abspath(__file__)

    # Переходим в родительский каталог (video_to_01)
    project_directory = os.path.dirname(os.path.dirname(script_path))
    os.chdir(project_directory)

    # Собираем полные пути к входному файлу и выходной папке относительно пути к проекту
    input_file = os.path.join(project_directory, input_file)
    output_folder = os.path.join(project_directory, output_folder)

    # Читаем данные из txt файла
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Создаем изображения на основе данных
    for i, line in enumerate(lines):
        frame_data = np.array(eval(line.replace('{', '[').replace('}', ']')))  # Преобразуем строку в массив
        frame_data = frame_data.reshape((64, 128))  # Восстанавливаем форму массива
        
        # Создаем изображение
        frame_image = np.zeros((64, 128), dtype=np.uint8)
        frame_image[frame_data == 1] = 255  # Устанавливаем белый цвет для пикселей со значением 1

        # Инвертируем изображение (черный фон)
        frame_image = cv2.bitwise_not(frame_image)

        # Сохраняем изображение
        image_path = f"{output_folder}/reconstructed_frame_{i}.png"
        cv2.imwrite(image_path, frame_image)

    print(f"Изображения созданы в {output_folder}")

input_file = "3_image_to_text/output.txt"
output_folder = "x_text_to_image/reconstructed_images"
create_images(input_file, output_folder)
