from moviepy.editor import VideoFileClip
from moviepy.video.fx import speedx  # Импортируем функцию speedx


# Путь к входному и выходному файлу
input_path = "U:\\TL_MDRK\\lte_010-eb438663de_1737648000_18030.mp4"
output_path = "U:\\TL_MDRK\\lte_010-eb438663de_1737648000_18030_.mp4"

# Загрузить видео
clip = VideoFileClip(input_path)

# Рассчитать коэффициент ускорения
duration = clip.duration
if duration <= 60:
    print("Видео уже короче или равно 1 минуте.")
    clip.write_videofile(output_path, codec="libx264", preset="medium", fps=24)
else:
    speed_factor = duration / 60

    # Ускорить видео
    final_clip = speedx.speedx(clip, speed_factor)

    # Сохранить результат
    final_clip.write_videofile(output_path, codec="libx264", preset="medium", fps=24)

    print(f"Видео ускорено в {round(speed_factor, 2)} раза и сохранено как {output_path}")




