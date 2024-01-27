# Перевод видео в формат, аналогичный GLCD 128x64

Этот проект представляет собой простое приложение для обработки видеофайлов. Приложение состоит из трех этапов:

1. **Изменение частоты кадров**: Видеофайл изменяется так, чтобы его частота кадров составляла 24 кадра в секунду.

2. **Разделение видео на кадры**: Видео разбивается на отдельные кадры, которые сохраняются в формате изображений.

3. **Анализ цветов кадров**: Каждый кадр анализируется на предмет цветов, и результаты сохраняются в текстовый документ.

## Использование

1. Запустите приложение `main.py`.
2. Выберите видеофайл для обработки.
3. Нажмите "Начать обработку" для выполнения трех этапов обработки.
4. Результаты каждого этапа отображаются в статусной строке.

## Дополнительные этапы

В проекте также присутствуют два дополнительных этапа:

4. **Текст в изображения**: Создание изображений на основе текстовых данных.

5. **Изображения в видео**: Создание видео на основе изображений.

Для выполнения дополнительных этапов нажмите "Проверить результат" после выполнения основных этапов.

## Просмотр результатов

- **Текстовый документ**: После завершения обработки, нажмите "Просмотреть результат" для просмотра текстового документа.
- **Видеоплеер**: После выполнения всех этапов, нажмите "Просмотреть результат" для просмотра созданного видео.

## Интеграция с GLCD Экраном (Планируется)

В будущем планируется связать этот проект с выводом изображения на GLCD экран 128x64 с помощью текстового документа с цветами. Полученные цветовые данные будут считываться микроконтроллером, который затем будет выводить изображения на экран GLCD.

## Зависимости

- Python 3
- OpenCV (`pip install opencv-python`)

