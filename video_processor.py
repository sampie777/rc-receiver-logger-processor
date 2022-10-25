import logging
from typing import Callable, Tuple

import cv2

logger = logging.getLogger(__name__)

def video_processor_create(output_file: str, frame_rate: int, resolution: Tuple[int, int],
                           create_frame_callback: Callable, cargs=()):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_file, fourcc, frame_rate, resolution)

    frame_index = 0
    while True:
        try:
            frame = create_frame_callback(frame_index, *cargs)
        except Exception as e:
            logger.exception(e, exc_info=True)
            break

        if frame is None:
            break

        video.write(frame)
        frame_index += 1

    video.release()
