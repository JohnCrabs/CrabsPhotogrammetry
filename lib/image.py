import os
from lib.message_handling import *


class ImageInfo:
    def __init__(self):
        self.src = ""
        self.dir = ""
        self.name = ""
        self.suffix = ""
        self.width = 0
        self.height = 0
        self.color_bands = 1

    def set_image_path(self, src):
        self.src = src
        self.dir = os.path.dirname(self.src)
        basename = os.path.splitext(os.path.basename(self.src))
        self.name = basename[0]
        self.suffix = basename[1]

    def set_image_size(self, width, height, color_bands):
        self.width = width
        self.height = height
        self.color_bands = color_bands

    def print_image_info(self):
        print("")
        print("full path:", self.src)
        print("directory:", self.dir)
        print("name:", self.name)
        print("suffix:", self.suffix)
        print("width:", self.width)
        print("height:", self.height)
        print("color bands:", self.color_bands)


class Image:
    def __init__(self):
        self.info = ImageInfo()

    def img_import(self, src: str):
        """
        Take the given src and import it to the self.info object.
        :param src: The path of the video
        :return: True/False
        """
        if os.path.exists(src):
            message_print("Open Video at " + src)
            self.info.set_image_path(src=src)
            return True
        return False

    def img_print_info(self):
        self.info.print_image_info()
