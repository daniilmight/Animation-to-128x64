import cv2
import os

def images_to_video(input_folder, output_video):
    # Получаем текущий путь к скрипту
    script_path = os.path.abspath(__file__)

    # Переходим в родительский каталог (video_to_01)
    project_directory = os.path.dirname(os.path.dirname(script_path))
    os.chdir(project_directory)

    # Собираем полные пути к входной папке и выходному видео относительно пути к проекту
    input_folder = os.path.join(project_directory, input_folder)
    output_video = os.path.join(project_directory, output_video)

    # Получаем список файлов изображений в указанной папке
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
    
    # Используем ключ сортировки для сортировки файлов по номерам кадров
    image_files.sort(key=lambda x: int(x.split('_')[2].split('.')[0]))

    # Определяем размер изображения на основе первого файла
    first_image = cv2.imread(os.path.join(input_folder, image_files[0]))
    height, width, layers = first_image.shape

    # Создаем объект VideoWriter с частотой кадров 24
    video_writer = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), 24, (width, height))

    # Добавляем изображения в видео
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        image = cv2.imread(image_path)
        video_writer.write(image)

    # Закрываем объект VideoWriter
    video_writer.release()

    print(f"Видео создано: {output_video}")

# Пример использования с относительными путями
input_folder = "x_text_to_image/reconstructed_images"
output_video = "x_image_to_video/output_video.mp4"
images_to_video(input_folder, output_video)
