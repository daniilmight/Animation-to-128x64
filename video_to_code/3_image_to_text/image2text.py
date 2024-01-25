import cv2
import os

def analyze_frames(input_folder, output_file):
    frames = []
    
    # Получаем текущий путь к скрипту
    script_path = os.path.abspath(__file__)

    # Переходим в родительский каталог (video_to_01)
    project_directory = os.path.dirname(os.path.dirname(script_path))
    os.chdir(project_directory)

    # Собираем полные пути к входной папке и выходному файлу относительно пути к проекту
    input_folder = os.path.join(project_directory, input_folder)
    output_file = os.path.join(project_directory, output_file)

    # Получаем список всех файлов в указанной папке и сортируем их по именам
    image_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.png')], key=lambda x: int(x.split('_')[1].split('.')[0]))
    
    num_frames = len(image_files)
    
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        # Читаем изображение
        image = cv2.imread(image_path)
        
        # Преобразуем изображение в оттенки серого
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Анализируем цвет каждого пикселя
        analyzed_frame = []
        for row in range(gray_image.shape[0]):
            for col in range(gray_image.shape[1]):
                pixel_value = gray_image[row, col]
                
                # Определяем, ближе ли цвет к белому (значение 255) или к черному (значение 0)
                if pixel_value > 127:  # 127 - пороговое значение
                    analyzed_frame.append(0)
                else:
                    analyzed_frame.append(1)
        
        frames.append(analyzed_frame)

    # Сохраняем массивы в txt файл
    with open(output_file, 'w') as f:
        for frame in frames:
            f.write(f"{{{', '.join(map(str, frame))}}}\n")  # Изменили [] на {}

    print(f"Анализ {num_frames} кадров завершен. Результаты сохранены в {output_file}")

# Пример использования с относительными путями
input_folder = "2_video24_to_image/images"
output_file = "3_image_to_text/output.txt"
analyze_frames(input_folder, output_file)
