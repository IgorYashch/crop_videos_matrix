import os
import json
import argparse
import numpy as np
from moviepy.editor import *


def create_clip(video,
                time_start=0, time_end=None,
                top_left_x=0, top_left_y=100, width=500, height=500,
                fontsize=30,
                name=None):
    if not name:
        name = os.path.basename(video).split('.')[0]

    clip = VideoFileClip(video)

    if time_end:
        if clip.duration < time_end or clip.duration < time_start:
            raise ValueError("Uncorrect times of start and end")
        clip = clip.subclip(time_start, time_end)

    clip = clip.crop(x1=top_left_x, y1=top_left_y,
                     x2=top_left_x + width,
                     y2=top_left_y + height)
    result = clip
    text_x, text_y = clip.size[0] // 100, clip.size[1] // 100
    txt_clip = TextClip(txt=name,
                        fontsize=fontsize, font="Arial-Bold",
                        color='white',
                        stroke_color='black', stroke_width=1.5,
                        ).set_duration(clip.duration)

    txt_clip = txt_clip.set_pos((text_x, text_y))

    result = CompositeVideoClip([clip, txt_clip])
    return result


def resize_list(lst, n):
    result = []
    for i in range(0, len(lst), n):
        result.append(lst[i: i + n])
    return result


def main():
    parser = argparse.ArgumentParser(description="Build crop matrix")
    parser.add_argument('--video_folder', type=str,
                        help="Folder with PNG images", required=True)
    parser.add_argument('--options', type=str,
                        help="Path to JSON with options", required=True)
    parser.add_argument('--ignore_time', action='store_false',
                        help='Don\'t cut video')

    args = parser.parse_args()

    # Read options
    with open(args.options, "r") as f:
        config = json.load(f)

    x = config["top_left_x"]
    y = config["top_left_y"]
    width = config["width"]
    height = config["height"]
    rows = config["rows"]
    columns = config["columns"]
    fontsize = config["fontsize"]
    time_start = config["time_start"]
    time_end = config["time_end"] if args.ignore_time else None

    videos = os.listdir(args.video_folder)

    clips_list = []

    for video in videos:
        video_path = os.path.join(args.video_folder, video)
        clip = create_clip(video_path, time_start=time_start, time_end=time_end,
                           top_left_x=x, top_left_y=y, width=width, height=height, fontsize=fontsize)
        clips_list.append(clip)

    black_clip = ColorClip(
        clips_list[0].size, (0, 0, 0), duration=clips_list[0].duration)

    if len(clips_list) > rows * columns:
        raise ValueError("Uncorrect number of rows and columns")
    else:
        clips_list = clips_list + [black_clip] * \
            (rows * columns - len(clips_list))

    clips_list = resize_list(clips_list, rows)

    final = clips_array(clips_list)
    final.write_videofile("result.mp4")


if __name__ == "__main__":
    main()
