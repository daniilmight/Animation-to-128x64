import cv2
import os

def split_frames(video_path, output_folder):
    # Получаем текущий путь к скрипту
    script_path = os.path.abspath(__file__)

    # Переходим в родительский каталог (video_to_01)
    project_directory = os.path.dirname(os.path.dirname(script_path))
    os.chdir(project_directory)

    # Собираем полные пути к видео и папке для сохранения изображений относительно пути к проекту
    video_path = os.path.join(project_directory, video_path)
    output_folder = os.path.join(project_directory, output_folder)

    # Открываем видеофайл
    cap = cv2.VideoCapture(video_path)

    frame_count = 0

    # Читаем кадры, уменьшаем их размер и сохраняем в виде изображений
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Уменьшаем размер кадра до 128x64
        resized_frame = cv2.resize(frame, (128, 64))

        frame_path = os.path.join(output_folder, f"frame_{frame_count}.png")
        cv2.imwrite(frame_path, resized_frame)

        frame_count += 1

    cap.release()

    print(f"Кадры сохранены в {output_folder}")

video_path = "1_video_to_24fps/video_24fps.mp4"
output_folder = "2_video24_to_image/images"
split_frames(video_path, output_folder)
