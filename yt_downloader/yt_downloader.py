import pafy
import cv2
import time
import multiprocessing as mp
import argparse
import os
import json

SUPPORT_URL_TYPE = ["youtube", "youtube-dl"]
class YotubeDownloader:
    def __init__(self, arguments: dict) -> None:
        self.url = arguments["url"]
        self.url_type = arguments["url_type"]
        if self.url_type not in SUPPORT_URL_TYPE:
            raise ValueError(f'url_type: {self.url_type} not supported. '
                             f'Please see README.md for more info.')

        self.output_path = self._build_output_folder(arguments["folder_name"])
        self.is_live = arguments["is_live"]
        self.frame_per_sec = arguments["extract_frames_per_second"]

        que_size = 2 if self.is_live else 5000
        que = mp.Queue(maxsize=que_size)

        self.reader = mp.Process(
            target=self._read_stream, args=(self.url, que,))
        self.writer = mp.Process(target=self._write_frames, args=(que,))

    def _build_output_folder(self, folder_name: str) -> str:
        """ Make the output folder for downloaded images.

            Make output folder under `dataset` folder. If the folder is already
            exist, this function will pause for 5 seconds for user to confirm.

            Args:
                folder_name: Name of output folder.

            Returns:
                output_path: Output path.
        """
        cur_path = os.path.realpath(__file__)
        cur_path = os.path.split(cur_path)[0]
        output_path = os.path.join(cur_path, "dataset", folder_name)
        if os.path.isdir(output_path):
            print(f"Folder {output_path} is already exists.")
            print(f"Make sure you want to download new frames into the "
                  f"same folder")
            time.sleep(5)
        os.makedirs(output_path, exist_ok=True)
        return output_path

    def start(self) -> None:
        """ Start downloading and writing frames.
        """
        print("Start downloading")
        self.reader.start()
        self.writer.start()
        self.reader.join()
        self.writer.join()

    def _read_stream(self, url: str, que: mp.Queue) -> None:
        """ Read youtube stream frames and put to queue.

            This function will handle different url type and different media
            type (video/live stream).

            For youtube, this function will connect it through pafy to obtain
            the best quality. For youtube-dl otherwise, it will be connected
            directly by opencv.

            For offline video, frame drop is handled by this function by
            calculating the drop frame interval with FPS. For live stream,
            frame drop is handled by frame writer.

            Args:
                url: Url set in config file.
                que: Output queue.

            Returns:
                None
        """
        capture = None
        while not capture or not capture.isOpened():
            if self.url_type == 'youtube':
                video = pafy.new(url)
                best = video.getbest()
                url = best.url
            capture = cv2.VideoCapture(url)
            print(f"{time.time()}:Opening youtube video.")
            time.sleep(.5)
        print(f"Successfully opened youtube video.")

        if self.is_live:
            while capture.isOpened():
                ret, frame = capture.read()
                if not ret:
                    continue
                if que.full():
                    que.get()
                que.put(frame)
        else:
            fps = capture.get(cv2.CAP_PROP_FPS)
            drop_frame_interval = int(fps / self.frame_per_sec)
            frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
            while capture.isOpened() and \
                    capture.get(cv2.CAP_PROP_POS_FRAMES) < frame_count:
                for _ in range(drop_frame_interval):
                    ret, frame = capture.read()
                if ret:
                    que.put(frame)

    def _write_frames(self, que: mp.Queue) -> None:
        """ Read frames from queue and write to files.

            Read frames from queue and write to files. The output filename
            will be timestamps.

            Args:
                que: Input queue.

            Returns:
                None
        """
        if self.is_live:
            sleep_time = 1 / self.frame_per_sec
        while True:
            if self.is_live:
                time.sleep(sleep_time)
            if not que.empty():
                frame = que.get()
                cur_ts = time.time()
                output_file = os.path.join(self.output_path, f"{cur_ts}.jpg")
                cv2.imwrite(output_file, frame)
                print(f"write frame {cur_ts}")


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to config file.",
                        default="config.json")
    config_file = open(parser.parse_args().config, 'r')
    config = json.loads(config_file.read())
    config_file.close()
    return config


def main():
    args = arg_parser()
    downloader = YotubeDownloader(args)
    downloader.start()


if __name__ == "__main__":
    main()
