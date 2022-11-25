#!/usr/bin/env python

import subprocess
import clize
from IPython import embed


def shell_require(args):
    print(args)
    proc = subprocess.run(args)
    proc.check_returncode()


def av_replace_video(input_av, input_v, output_av):
    args = [
        'ffmpeg',
        '-i', input_av,
        '-i', input_v,
        '-map', '1:a',
        '-map', '0:v',
        output_av
    ]

    shell_require(args)


def av_rescale_video(
        input_av,
        output_av,
        *args,
        start_at=None,
        end_at=None
):

    if start_at is not None:
        start_at = ['-ss', start_at]
    else:
        start_at = []

    if end_at is not None:
        end_at = ['-to', end_at]
    else:
        end_at = []

    args = [
        'ffmpeg',
        '-i', input_av,
        '-c:v', 'libx264', '-crf', '23',
        '-vf', 'scale=1920:1080',
        *start_at,
        *end_at,
        *args,
        output_av
    ]

    shell_require(args)



def av_timelapse(input_pattern: str, output_path: str, start_number: int, fps: int = 30, crf: int = 17, *, intra: bool = False):
    args = [
        'ffmpeg', 
        '-framerate', str(fps),
        '-start_number', str(start_number),
        '-i', input_pattern,
        '-c:v', 'libx264', 
        '-crf', str(crf),
        *(['-intra'] if intra else []),
        output_path
    ]

    shell_require(args)



def shell():
    embed(colors="neutral")


clize.run([
    shell,
    av_replace_video,
    av_rescale_video,
    av_timelapse
])
