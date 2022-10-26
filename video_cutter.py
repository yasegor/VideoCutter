import os
import random
import time

from moviepy.editor import *


def get_info() -> tuple:
    """
    Тут мы получаем информацию от пользователя.
    Длительность видео, качество, путь к видео, путь к музыке.
    """
    interval = input('Введите интервал видео через тире (например: 45-60): \n').split("-")
    quality = int(input('Введите желаемое разрешение видео (например: 720 или 1080):\nДоступно от 240р до 1080р\n'))
    folders_count = int(input("Введите желаемое количество папок на выходе: \n"))
    threads = int(input("Введите количество потоков в процессоре: \n"))

    try:
        videos_path = input('Введите путь к папке с видеороликами:\n')
        if not os.path.exists(videos_path):
            raise IOError
        music_path = input('Введите путь к папке с музыкой:\n')
        if not os.path.exists(music_path):
            raise IOError

        return interval, quality, threads, folders_count, videos_path, music_path
    except IOError:
        print("\033[1m\033[31m{}\033[0m".format('[INFO] Такого пути не существует!'))


def working_process(quality: int, interval: list, threads: int, folders_count: int, main_folder: str, videos_path: str,
                    videos_list: list,
                    music_path: str, music_list: list):
    """
    Тут идёт рабочий процесс.
    Мы проходимся по каждому видео в папке, получаем его длительность и сравниваем не выходит ли она за интервал.
    Собираем список с инстансами в один большой список.
    Собираем список с названиями в один большой список. Списки в списке.
    """
    print("\033[1m\033[33m{}\033[0m".format("[INFO] Отправляем видео на редактирование, ожидайте..."))
    start_num = 1
    end_num = 1
    counter = 0
    folders_num = 0
    one_video = list()
    videos_instances = list()
    one_video_names = list()
    videos_names = list()
    min_sec, max_sec = list(map(int, interval))

    for video in range(1, len(videos_list) + 1):

        if folders_count > 0 and folders_num == folders_count:
            break

        try:
            clip = VideoFileClip(fr"{videos_path}\{videos_list[video - 1]}").resize(height=quality)
            duration = clip.duration
            if counter + duration < max_sec:
                counter += duration
                one_video.append(clip)
                one_video_names.append(videos_list[video - 1])
            elif counter < min_sec:
                clip = clip.subclip(0, max_sec - counter)
                counter += clip.duration
                one_video.append(clip)
                one_video_names.append(videos_list[video - 1])
            elif duration > max_sec:
                clip.subclip(0, max_sec)
                one_video.append(clip)
                one_video_names.append(videos_list[video - 1])
            else:
                videos_instances.append(one_video)
                videos_names.append(one_video_names)
                one_video = list()
                one_video_names = list()
                counter = 0
                one_video.append(clip)
                one_video_names.append(videos_list[video - 1])
                counter += duration
            clip.close()

            if len(videos_instances) == 14 or video == len(videos_list):
                if video == len(videos_list):
                    end_num = start_num + len(videos_instances) + 1
                    videos_instances.append(one_video)
                    videos_names.append(one_video_names)
                else:
                    end_num = start_num + 14
                sub_folder = folder_creator(start_num, end_num, main_folder)
                folders_num += 1
                start_num += 15
                edit_video(videos_instances, music_list, music_path, videos_names, sub_folder, threads)
                one_video = list()
                one_video_names = list()
                videos_instances = list()
                videos_names = list()
                counter = 0
        except OSError:
            print("\033[1m\033[31m{}\033[0m".format("[!!! INFO !!!] Ошибка системы, продолжаю работу...\n"))


def edit_video(videos_instances: list, music_list: list, music_path: str, videos_names: list, sub_folder: str,
               threads: int):
    """
    Тут происходит склеивание инстансов нескольких видео в один полноценный клип.
    У каждого клипа удаляется оригинальная звуковая дорожка.
    Добавляется музыка из предварительного перемешанного списка .
    """
    print("\033[1m\033[32m{}\033[0m".format("[INFO] Перемешиваю музыку..."))

    random_music = random.sample(music_list, len(videos_instances))

    print("\033[1m\033[36m{}\033[0m".format("[INFO] Начинаем склеивание видео..."))

    for list_num in range(len(videos_instances)):

        print("\033[1m\033[35m{}\033[0m".format(f"[INFO] Делаю {list_num + 1}-е видео из..."))
        print("\033[1m\033[36m{}\033[0m".format(videos_names[list_num]))
        try:
            full_clip = concatenate_videoclips(videos_instances[list_num], method='compose')
            full_clip.without_audio()
            audio_clip = AudioFileClip(fr"{music_path}\{random_music[list_num]}").subclip(0, full_clip.duration)
            final_clip = full_clip.set_audio(audio_clip).audio_fadein(1).audio_fadeout(1)
            final_clip.write_videofile(fr"{sub_folder}\{list_num + 1}.mp4", fps=30, threads=threads)
            final_clip.close()

        except OSError:
            print("\033[1m\033[31m{}\033[0m".format("[!!! INFO !!!] Ошибка системы, продолжаю работу...\n"))


def video_15s(main_folder: str, threads=2):
    """
    Тут создаётся последнее финальное видео - склейка всех предыдущих готовых видео. Аудио не редактируется.
    """
    print("\033[1m\033[36m{}\033[0m".format("[INFO] Начинаю склеивать последние видеоролики..."))

    folders_list = os.listdir(main_folder)
    for folder in folders_list:

        print("\033[1m\033[35m{} {}\033[0m".format(f"[INFO] Создаю видеоролик в папке:", folder))

        videos_list = os.listdir(fr"{main_folder}\{folder}")
        instances = list()
        for video in videos_list:
            clip = VideoFileClip(fr"{main_folder}\{folder}\{video}")
            instances.append(clip)
        clip_15s = concatenate_videoclips(instances, method='compose')
        clip_15s.write_videofile(fr"{main_folder}\{folder}\{len(videos_list) + 1}.mp4", threads=threads)

    print("\033[1m\033[32m{}\033[0m".format("[CONGRATULATIONS] Работа скрипта завершена успешно!"))


def folder_creator(start_num: int, end_num: int, main_folder: str) -> str:
    """
    Тут создается папка с названием видео в формате "от" и "до".
    """
    print("\033[1m\033[34m{} {}-{}\033[0m".format("Создаем подпапку", start_num, end_num))

    os.mkdir(fr"{main_folder}\{start_num}-{end_num}")
    sub_folder = fr"{main_folder}\{start_num}-{end_num}"
    return sub_folder


def main():
    print("\033[1m\033[33m{} \033[34m{}\033[0m".format("Script was created by", "https://github.com/yasegor"))
    time.sleep(5)

    actual_path = os.getcwd()
    main_folder = fr"{actual_path}\final_videos"

    if not os.path.exists(main_folder):
        interval, quality, threads, folders_count, videos_path, music_path = get_info()

        videos_list = os.listdir(videos_path)
        music_list = os.listdir(music_path)

        video_resolution = {240: 426, 360: 640, 480: 854, 720: 1280, 1080: 1920}

        try:
            quality = video_resolution[quality]
        except KeyError as e:
            print(e)
            print("\033[1m\033[31m{}\033[0m".format("Введён неверный формат разрешения. "
                                                    "Повторите снова в форме 720 или 1080, без доп. символов.\n"))
            quality = int(input('Введите желаемое разрешение видео (например: 720 или 1080): \n '
                                'Доступно от 240р до 1080р\n'))
            quality = video_resolution[quality]

        print("\033[1m\033[34m{}\033[0m".format("[INFO] Создаём папку final_videos..."))

        os.mkdir(main_folder)

        working_process(quality=quality, interval=interval, threads=threads, folders_count=folders_count,
                        main_folder=main_folder,
                        videos_path=videos_path, videos_list=videos_list, music_path=music_path, music_list=music_list)

        video_15s(main_folder, threads=threads)
    else:
        video_15s(main_folder)


if __name__ == "__main__":
    main()
