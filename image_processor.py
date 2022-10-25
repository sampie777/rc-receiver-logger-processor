from typing import Tuple, Optional, List

import numpy
from PIL import Image, ImageDraw
from PIL.Image import Image as ImageType

from objects import Reading

next_frame_time = 0
last_frame = None
background_color = (50, 50, 0)

joystick_center = (960, 900)
joystick_spacing = 500
joystick_knob_radius = 68 / 2
joystick_base_radius = 212 / 2

joystick_base_image: Optional[ImageType] = None
joystick_knob_image: Optional[ImageType] = None


def init(resolution: Tuple[int, int]):
    global joystick_base_image, joystick_knob_image
    joystick_base_image = Image.open("assets/joystick-base.png")
    joystick_knob_image = Image.open("assets/joystick-knob.png")


def close():
    if joystick_base_image is not None:
        joystick_base_image.close()
    if joystick_knob_image is not None:
        joystick_knob_image.close()


def draw_centered(base_image: ImageType, image: ImageType, center: Tuple[float, float]):
    corner = (round(center[0] - image.size[0] / 2), round(center[1] - image.size[1] / 2))
    base_image.paste(image, corner, image)


def draw_joystick(image: ImageType, center: Tuple[float, float], knob_offset: Tuple[float, float]):
    knob_center = (center[0] + (joystick_base_radius - joystick_knob_radius) * knob_offset[0],
                   center[1] + (joystick_base_radius - joystick_knob_radius) * knob_offset[1])

    draw_centered(image, joystick_base_image, center)
    draw_centered(image, joystick_knob_image, knob_center)


def create_frame(frame_index, reading: Reading, frame_rate: int, resolution: Tuple[int, int]) -> List:
    global next_frame_time, last_frame
    frames = []

    if joystick_knob_image is None or joystick_base_image is None:
        raise Exception("Joystick images are not initialized. Did you forget to call init()?")

    if next_frame_time == 0:
        next_frame_time = reading.timestamp

    if reading.timestamp < next_frame_time:
        return frames

    next_frame_time += + 1000 / frame_rate
    while reading.timestamp > next_frame_time:
        next_frame_time += + 1000 / frame_rate
        frames.append(last_frame)

    image = Image.new('RGB', resolution, background_color)

    left_x = -1 * min(1.0, max(-1.0, reading.channel4 * 2 - 1))
    left_y = -1 * min(1.0, max(-1.0, reading.channel3 * 2 - 1))
    right_x = -1 * min(1.0, max(-1.0, reading.channel1 * 2 - 1))
    right_y = -1 * min(1.0, max(-1.0, reading.channel2 * 2 - 1))

    draw_joystick(image, (joystick_center[0] - joystick_spacing / 2, joystick_center[1]), (left_x, left_y))
    draw_joystick(image, (joystick_center[0] + joystick_spacing / 2, joystick_center[1]), (right_x, right_y))

    ImageDraw.Draw(image).text((100, 100), "{} ms".format(reading.timestamp))

    # image.show()
    # raise Exception("Bye")

    last_frame = numpy.array(image)
    frames.append(last_frame)
    return frames
