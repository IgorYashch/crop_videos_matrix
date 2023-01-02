# Скрипт для построения матрицы кропов (для видео)
Пример использования: 
``` python
python build_crop_video_matrix.py --video_folder ./videos --options ./options.json --ignore_time
```
Аргументы:
``` python
image_folder -- путь до папки с видео (в папке должны быть только видео)

options -- путь до JSON файла с опциями, имеющего вид:

{
    "top_left_x" : 750, # Координаты левого верхнего угла кропа
    "top_left_y" : 180,
    "width" : 320,      # Размеры кропа
    "height" : 270,
    "rows" : 3,         # Количество кропов в столбце
    "columns" : 3,      # Количество кропов в строке
    "fontsize" : 36     # Размер шрифта названий
    "time_start": 0,    # Время начала фрагмента (в секундах)
    "time_end" : 2      # Время конца фрагмента (в секундах)
}

ignore_time -- устанавливается, если нет необходимости обрезать видео по времени
```

Названия берутся из названий видео.
Результат будет записан в ./result.mp4.

Пример:<br>
![ezgif com-gif-maker](https://user-images.githubusercontent.com/100944349/210284534-bfbc8a33-5100-456f-a5b3-4e14034dbd39.gif)


### Требования

* python
* numpy
* moviepy
* ffmpeg
