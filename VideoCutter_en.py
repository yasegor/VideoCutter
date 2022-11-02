import os
import random
import time

from moviepy.editor import *


def get_info() -> tuple:
    """
    Here we receive information from the user.
    Video duration, quality, path to video, path to music.
    """
    interval = input('Enter the video interval through a dash (for example: 45-60): \n').split("-")
    quality = int(input('Enter your desired video resolution (for example: 720 or 1080):\nAvailable from 240p to 1080p\n'))
    folders_count = int(input("Enter the desired number of output folders: \n"))
    threads = int(input("Enter the number of threads in the processor: \n"))

    try:
        videos_path = input('Enter the path to the video folder:\n')
        if not os.path.exists(videos_path):
            raise IOError
        music_path = input('Enter the path to the music folder:\n')
        if not os.path.exists(music_path):
            raise IOError

        return interval, quality, threads, folders_count, videos_path, music_path
    except IOError:
        print("\033[1m\033[31m{}\033[0m".format('[INFO] There is no such path!'))


def working_process(quality: int, interval: list, threads: int, folders_count: int, main_folder: str, videos_path: str,
                    videos_list: list,
                    music_path: str, music_list: list):
    """
    Here is the workflow.
    We iterate over each video in the folder, get its duration, and compare whether it goes beyond the interval.
    We collect the list with instances into one big list.
    We collect the list with names in one big list. Lists in a list.
    """
    print("\033[1m\033[33m{}\033[0m".format("[INFO] Submitting the video for editing, please wait..."))
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
            print("\033[1m\033[31m{}\033[0m".format("[!!! INFO !!!] System error, keep going...\n"))


def edit_video(videos_instances: list, music_list: list, music_path: str, videos_names: list, sub_folder: str,
               threads: int):
    """
    Here the instances of several videos are merged into one full-fledged clip.
    The original audio track is removed from each clip.
    Added music from the pre-shuffled list.
    """
    print("\033[1m\033[32m{}\033[0m".format("[INFO] Shuffling music..."))

    random_music = random.sample(music_list, len(videos_instances))

    print("\033[1m\033[36m{}\033[0m".format("[INFO] Let's start making videos..."))

    for list_num in range(len(videos_instances)):

        print("\033[1m\033[35m{}\033[0m".format(f"[INFO] Making the {list_num + 1}th video from..."))
        print("\033[1m\033[36m{}\033[0m".format(videos_names[list_num]))
        try:
            full_clip = concatenate_videoclips(videos_instances[list_num], method='compose')
            full_clip.without_audio()
            audio_clip = AudioFileClip(fr"{music_path}\{random_music[list_num]}").subclip(0, full_clip.duration)
            final_clip = full_clip.set_audio(audio_clip).audio_fadein(1).audio_fadeout(1)
            final_clip.write_videofile(fr"{sub_folder}\{list_num + 1}.mp4", fps=30, threads=threads)
            final_clip.close()

        except OSError:
            print("\033[1m\033[31m{}\033[0m".format("[!!! INFO !!!] System error, keep going...\n"))


def video_15s(main_folder: str, threads=2):
    """
    Here the last final video is created - merging all previous finished videos. Audio is not edited.
    """
    print("\033[1m\033[36m{}\033[0m".format("[INFO] I'm putting together the latest videos..."))

    folders_list = os.listdir(main_folder)
    for folder in folders_list:

        print("\033[1m\033[35m{} {}\033[0m".format(f"[INFO] Creating a video in the folder:", folder))

        videos_list = os.listdir(fr"{main_folder}\{folder}")
        instances = list()
        for video in videos_list:
            clip = VideoFileClip(fr"{main_folder}\{folder}\{video}")
            instances.append(clip)
        clip_15s = concatenate_videoclips(instances, method='compose')
        clip_15s.write_videofile(fr"{main_folder}\{folder}\{len(videos_list) + 1}.mp4", threads=threads)

    print("\033[1m\033[32m{}\033[0m".format("[CONGRATULATIONS] Script completed successfully!"))


def folder_creator(start_num: int, end_num: int, main_folder: str) -> str:
    """
    This creates a folder with the name of the video in the format "from" and "to".
    """
    print("\033[1m\033[34m{} {}-{}\033[0m".format("Creating subfolder", start_num, end_num))

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
            print("\033[1m\033[31m{}\033[0m".format("Invalid resolution format entered. "
                                                    "Repeat again in the form 720 or 1080, without any additional characters.\n"))
            quality = int(input('Enter your desired video resolution (for example: 720 or 1080): \n '
                                'Available from 240p to 1080p\n'))
            quality = video_resolution[quality]

        print("\033[1m\033[34m{}\033[0m".format("[INFO] Creating folder final_videos..."))

        os.mkdir(main_folder)

        working_process(quality=quality, interval=interval, threads=threads, folders_count=folders_count,
                        main_folder=main_folder,
                        videos_path=videos_path, videos_list=videos_list, music_path=music_path, music_list=music_list)

        video_15s(main_folder, threads=threads)
    else:
        video_15s(main_folder)


if __name__ == "__main__":
    main()
