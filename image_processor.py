from typing import Tuple, Optional

import numpy
from PIL import Image, ImageFont, ImageDraw

from objects import Reading

next_frame_time = 0
background_color = (0, 0, 0)


def create_frame(frame_index, reading: Reading, frame_rate: int, resolution: Tuple[int, int]) -> Optional:
    global next_frame_time

    if reading.timestamp < next_frame_time:
        return None

    while reading.timestamp > next_frame_time:
        next_frame_time += 1000 / frame_rate

    image = Image.new('RGB', resolution, background_color)
    draw = ImageDraw.Draw(image)
    # font = ImageFont.truetype("sans-serif.ttf", 16)
    draw.text((0, 0), "Trottle: {} %".format(round(reading.channel3 * 100, 1)), (255, 255, 255))
    draw.text((0, 50), "Ailevator: {} %".format(round(reading.channel2 * 100, 1)), (255, 255, 255))
    draw.text((0, 100), "Rudder: {} %".format(round(reading.channel4 * 100, 1)), (255, 255, 255))

    return numpy.array(image)
