import glob
from typing import List, Optional

import cv2

from video_processor import video_processor_create

resolution = (1920, 1080)
frame_rate = 30
output_file = "output.avi"
input_file = "data-0.csv"


def create_frame(index: int, files: List[str]) -> Optional:
    if index > len(files):
        return None

    print("\rConverting... {} %".format(round(index / (len(files) - 1) * 100)), end="", flush=True)
    return cv2.imread(files[index])


def main():
    files = glob.glob("/media/samuel/Windows/Users/samuel/Pictures/*.png")
    video_processor_create(output_file, frame_rate, resolution, create_frame, (files,))


if __name__ == "__main__":
    main()
