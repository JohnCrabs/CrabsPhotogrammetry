import numpy as np
from lib.message_handling import *


class Camera:

    def __init__(self):
        self.fx = 1.0
        self.fy = 1.0
        self.cx = 0.0
        self.cy = 0.0

        self.exist = False
        self.mtrx = []

    def set_camera_parameters(self, f_x: float, f_y: float, c_x: float, c_y: float):
        self.fx = f_x
        self.fy = f_y
        self.cx = c_x
        self.cy = c_y

    def approximate_focal_length(self, width, height):
        if width > height:  # Check id width > height
            w = width  # Set w = width
        else:  # else
            w = height  # w = height
        focal = (0.7 * w + w) / 2  # Approximate the focal length as the the average of (70% of w + 100% of w)
        return focal

    def approximate_camera_parameters(self, width: int, height: int):
        focal = self.approximate_focal_length(width, height)
        self.fx = focal
        self.fy = focal
        self.cx = width / 2
        self.cy = height / 2

    def set_camera_matrix(self):
        self.exist = True
        cam_mtrx = ([self.fx, 0, self.cx],
                    [0, self.fy, self.cy],
                    [0, 0, 1])
        self.mtrx = np.array(cam_mtrx)

    def camera_info(self):
        print("")
        message_print("Camera Matrix = ")
        print(self.mtrx)
