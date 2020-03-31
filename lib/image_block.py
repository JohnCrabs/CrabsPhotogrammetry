from lib.image import *


class ImageBlock:
    def __init__(self):
        self.img_list = []

    def b_img_create_image_list(self, img_list):
        self.img_list = img_list

    def b_img_append_image_to_list(self, img: Image()):
        self.img_list.append(img)

    def b_img_match_all_images(self):
        pass

    def b_img_fast_matching(self):
        pass
