import logging
from typing import Callable, Tuple

import cv2

logger = logging.getLogger(__name__)


def init(output_file: str, frame_rate: int, resolution: Tuple[int, int]):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    return cv2.VideoWriter(output_file, fourcc, frame_rate, resolution)


def close(video):
    video.release()
