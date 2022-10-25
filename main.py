import logging
from typing import List, Tuple

import image_processor
import utils
import video_processor
from objects import Reading

logger = logging.getLogger(__name__)

resolution: Tuple[int, int] = (1920, 1080)
frame_rate: int = 30
input_file = "data-0.csv"


def convert_csv_data(data: List[str]) -> Reading:
    reading = Reading()
    reading.timestamp = int(data[0])
    reading.channel1 = float(data[1]) / 100
    reading.channel2 = float(data[2]) / 100
    reading.channel3 = float(data[3]) / 100
    reading.channel4 = float(data[4]) / 100
    reading.channel5 = float(data[5]) / 100
    reading.channel6 = float(data[6]) / 100
    reading.period1 = int(data[7])
    return reading


def process_csv(csv, file_line_count, video):
    print("\rProcessing ... 0 %", end="", flush=True)
    frame_index = 0
    for i, line in enumerate(csv):
        # Skip header line
        if i == 0:
            continue

        csv_data = line.split(";")
        try:
            reading = convert_csv_data(csv_data)
        except Exception as e:
            logger.error("Failed to convert data for frame {} for line '{}'".format(i, line))
            logger.exception(e, exc_info=True)
            break

        try:
            frames = image_processor.create_frame(frame_index, reading, frame_rate, resolution)
        except Exception as e:
            logger.error("Failed to create frame {} for line '{}'".format(i, line))
            logger.exception(e, exc_info=True)
            break

        for frame in frames:
            print("\rProcessing... {} %   ({} sec.)".format(round(i / (file_line_count - 1) * 100),
                                                            round(frame_index / frame_rate)), end="", flush=True)
            try:
                video.write(frame)
                frame_index += 1
            except Exception as e:
                logger.error("Failed to write frame {} for line '{}'".format(i, line))
                logger.exception(e, exc_info=True)
                break


def main():
    print("Data file: {}".format(input_file))
    output_file = "{}.avi".format(utils.remove_file_extension(input_file))
    print("Video file: {}".format(output_file))

    file_line_count = utils.file_line_count(input_file)
    image_processor.init(resolution)
    video = video_processor.init(output_file, frame_rate, resolution)

    try:
        with open(input_file, 'r') as csv:
            process_csv(csv, file_line_count, video)
    except KeyboardInterrupt as e:
        print("\nCancelling...")
        pass

    video_processor.close(video)
    image_processor.close()
    print("\nDone")


if __name__ == "__main__":
    main()
