import cv2
import os
import sys

def split_frames(video_path, output_folder):
    # Считываем путь к видео и папку для сохранения из командной строки
    if len(sys.argv) > 2:
        video_path = sys.argv[1]
        output_folder = sys.argv[2]

    # Получаем текущий путь к скрипту
    script_path = os.path.abspath(__file__)

    # Переходим в родительский каталог
    project_directory = os.path.dirname(os.path.dirname(script_path))
    os.chdir(project_directory)

    # Собираем полные пути к видео и папке для сохранения изображений относительно пути к проекту
    video_path = os.path.join(project_directory, video_path)
    output_folder = os.path.join(project_directory, output_folder)

    # Проверяем, существует ли папка, и создаем ее, если нет
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

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

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python video2image.py <video_path> <output_folder>")
        sys.exit(1)

    video_path = sys.argv[1]
    output_folder = sys.argv[2]

    split_frames(video_path, output_folder)
