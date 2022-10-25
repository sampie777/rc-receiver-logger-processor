from typing import Tuple, Optional, List

import numpy
from PIL import Image, ImageDraw
from PIL.Image import Image as ImageType

from objects import Reading

background_color = (50, 50, 0)

joystick_center = (960, 900)
joystick_spacing = 500
joystick_knob_radius = 68 / 2
joystick_base_radius = 212 / 2

_joystick_base_image: Optional[ImageType] = None
_joystick_knob_image: Optional[ImageType] = None

_next_frame_time = 0
_last_frame = None
_timestamp_offset = 0
_channels_activated = False

def init(resolution: Tuple[int, int]):
    global _joystick_base_image, _joystick_knob_image
    _joystick_base_image = Image.open("assets/joystick-base.png")
    _joystick_knob_image = Image.open("assets/joystick-knob.png")


def close():
    if _joystick_base_image is not None:
        _joystick_base_image.close()
    if _joystick_knob_image is not None:
        _joystick_knob_image.close()


def draw_centered(base_image: ImageType, image: ImageType, center: Tuple[float, float]):
    corner = (round(center[0] - image.size[0] / 2), round(center[1] - image.size[1] / 2))
    base_image.paste(image, corner, image)


def draw_joystick(image: ImageType, center: Tuple[float, float], knob_offset: Tuple[float, float]):
    knob_center = (center[0] + (joystick_base_radius - joystick_knob_radius) * knob_offset[0],
                   center[1] + (joystick_base_radius - joystick_knob_radius) * knob_offset[1])

    draw_centered(image, _joystick_base_image, center)
    draw_centered(image, _joystick_knob_image, knob_center)


def create_frame(frame_index, reading: Reading, frame_rate: int, resolution: Tuple[int, int]) -> List:
    global _next_frame_time, _last_frame, _timestamp_offset, _channels_activated
    frames = []

    if _joystick_knob_image is None or _joystick_base_image is None:
        raise Exception("Joystick images are not initialized. Did you forget to call init()?")

    # Filter out the first few seconds where the engine is cut off
    if not _channels_activated and reading.channel3 < 0:
        _timestamp_offset = reading.timestamp
        return frames

    # Only set channels as activated after the first data line which might contain useless data
    _channels_activated = frame_index != 0

    if _next_frame_time == 0:
        _next_frame_time = reading.timestamp - _timestamp_offset

    if reading.timestamp - _timestamp_offset < _next_frame_time:
        return frames

    _next_frame_time += + 1000 / frame_rate

    # Create repeating frames to cover up missing frames
    while reading.timestamp - _timestamp_offset > _next_frame_time:
        _next_frame_time += + 1000 / frame_rate
        frames.append(_last_frame)

    image = Image.new('RGB', resolution, background_color)

    left_x = -1 * min(1.0, max(-1.0, reading.channel4 * 2 - 1))
    left_y = -1 * min(1.0, max(-1.0, reading.channel3 * 2 - 1))
    right_x = -1 * min(1.0, max(-1.0, reading.channel1 * 2 - 1))
    right_y = -1 * min(1.0, max(-1.0, reading.channel2 * 2 - 1))

    draw_joystick(image, (joystick_center[0] - joystick_spacing / 2, joystick_center[1]), (left_x, left_y))
    draw_joystick(image, (joystick_center[0] + joystick_spacing / 2, joystick_center[1]), (right_x, right_y))

    ImageDraw.Draw(image).text((100, 100), "{} s".format(round(reading.timestamp / 1000, 1)))

    # image.show()
    # raise Exception("Bye")

    _last_frame = numpy.array(image)
    frames.append(_last_frame)
    return frames
