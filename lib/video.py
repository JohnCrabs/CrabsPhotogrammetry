import os
import cv2
import time
from lib.message_handling import *


class VideoInfo:
    def __init__(self):
        self.src = ""
        self.dir = ""
        self.dir_name = ""
        self.name = ""
        self.suffix = ""
        self.width = 0
        self.height = 0
        self.color_bands = 1
        self.fps = 0

    def set_video_info(self, src):
        self.set_video_path(src)
        video_cap = cv2.VideoCapture(self.src)
        self.fps = calc_fps_from_video(video_cap)

    def set_video_path(self, src):
        self.src = src
        self.dir = os.path.dirname(self.src)
        dir_name = os.path.normpath(self.dir)
        dir_name = dir_name.split(os.sep)
        self.dir_name = dir_name[len(dir_name)-1]
        basename = os.path.splitext(os.path.basename(self.src))
        self.name = basename[0]
        self.suffix = basename[1]

    def set_video_frame_size(self, width, height, color_bands):
        self.width = width
        self.height = height
        self.color_bands = color_bands

    def set_video_frame_rate(self, fps):
        self.fps = fps

    def print_video_info(self):
        print("")
        print("full path: ", self.src)
        print("directory: ", self.dir)
        print("directory name: ", self.dir_name)
        print("name: ", self.name)
        print("suffix: ", self.suffix)
        print("frame width: ", self.width)
        print("frame height: ", self.height)
        print("frame color bands: ", self.color_bands)
        print("frame per second (fps): ", self.fps)


class Video:
    def __init__(self):
        self.info = VideoInfo()

    def vid_open(self, src):
        """
        Using the given src and import it to the self.info object calculate the video information.
        :param src: The path of video.
        :return: True/False
        """
        if os.path.exists(src):
            message_print("Open Video at " + src)
            self.info.set_video_info(src=src)
            return True
        return False

    def vid_import(self, src: str):
        """
        Using the given src and import it to the self.info object read the video path information.
        :param src: The path of the video
        :return: True/False
        """
        if os.path.exists(src):
            message_print("Open Video at " + src)
            self.info.set_video_path(src=src)
            return True
        return False

    def vid_print_info(self):
        """
        Print the video path information in the console.
        :return: Nothing
        """
        self.info.print_video_info()


def calc_fps_from_video(video):
    """
    Calculates the fps of a given video.
    :param video: Open cv2.VideoCapture() object
    :return: fps
    """
    (major_ver, minor_ver, subminor_ver) = cv2.__version__.split('.')
    if int(major_ver) < 3:
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        # print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else:
        fps = video.get(cv2.CAP_PROP_FPS)
        # print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    if fps == 0:
        num_frames = 180
        start_time = time.time()
        for frame in range(0, num_frames):
            video.read()
        end_time = time.time()
        seconds = end_time - start_time
        fps = num_frames / seconds

    fps = int(round(fps, 1))
    return fps
