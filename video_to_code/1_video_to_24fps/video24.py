import cv2
import os

def change_frame_rate(input_video, output_video, target_frame_rate=24):
    # Получаем текущий путь к скрипту
    script_path = os.path.abspath(__file__)
    
    # Переходим в родительский каталог (video_to_01)
    project_directory = os.path.dirname(os.path.dirname(script_path))
    os.chdir(project_directory)

    # Собираем полные пути к входному и выходному видео относительно пути к проекту
    input_video = os.path.join(project_directory, input_video)
    output_video = os.path.join(project_directory, output_video)

    # Открываем видеофайл
    cap = cv2.VideoCapture(input_video)

    # Определяем размер изображения на основе первого кадра
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Создаем объект VideoWriter с целевой частотой кадров
    video_writer = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), target_frame_rate, (width, height))

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Записываем кадр в новое видео
        video_writer.write(frame)

    # Закрываем объекты VideoWriter и VideoCapture
    video_writer.release()
    cap.release()

    print(f"Видео создано с частотой кадров {target_frame_rate}: {output_video}")

# Пример использования с относительными путями
input_video = "1_video_to_24fps/video.mp4"
output_video = "1_video_to_24fps/video_24fps.mp4"
change_frame_rate(input_video, output_video, target_frame_rate=24)
