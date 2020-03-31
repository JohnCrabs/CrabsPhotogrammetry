import os
import cv2
from lib.message_handling import *
from lib.camera import *

class ImageInfo:
    def __init__(self):
        self.src = ""
        self.dir = ""
        self.dir_name = ""
        self.name = ""
        self.suffix = ""
        self.width = 0
        self.height = 0
        self.color_bands = 1

    def set_image_info(self, src):
        self.set_image_path(src)
        img = cv2.imread(self.src)
        if img is not None:
            img_size = img.shape
            self.width = img_size[1]
            self.height = img_size[0]
            self.color_bands = 1
            if len(img_size) == 3:
                self.color_bands = img_size[2]

    def set_image_path(self, src):
        self.src = os.path.normpath(src)
        self.dir = os.path.dirname(self.src)
        dir_name = os.path.normpath(self.dir)
        dir_name = dir_name.split(os.sep)
        self.dir_name = dir_name[len(dir_name) - 1]
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
        self.camera = Camera()

    def img_open(self, src: str):
        """
        Using the given src and import it to the self.info object calculate the image information.
        :param src: The path of image.
        :return: True/False
        """
        if os.path.exists(src):
            message_print("Open Image at " + src)
            self.info.set_image_info(src=src)
            return True
        return False

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

    def img_set_size(self, width, height, color_bands):
        self.info.set_image_size(width, height, color_bands)

    def img_print_info(self):
        self.info.print_image_info()

    def img_approximate_camera_parameters(self):
        self.camera.approximate_camera_parameters(self.info.width, self.info.height)
        self.camera.set_camera_matrix()

    def img_print_camera_matrix(self):
        message_print("Camera Info for Image " + self.info.name + ":")
        self.camera.camera_info()
