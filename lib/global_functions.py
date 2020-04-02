import cv2
from lib.image import *

def findMax_2x2(mtrx):
    x = 0
    y = 0

    for m in mtrx:
        if x < m[0]:
            x = m[0]
        if y < m[1]:
            y = m[1]
    return x, y

def find_color_list(img: Image(), pts_inlier: []):
    colors = []  # list to store the colors
    img_open = cv2.imread(img.info.src)  # open the image

    blue = img_open[:, :, 0]  # take blue channel
    green = img_open[:, :, 1]  # take green channel
    red = img_open[:, :, 2]  # take red channel

    # ------------------------------------------- #
    # Uncomment the necx lines for debugging
    # ------------------------------------------- #
    # cv.imwrite("./blue.jpg", blue)
    # cv.imwrite("./green.jpg", green)
    # cv.imwrite("./red.jpg", red)
    # cv.imwrite("./img.jpg", img_L_open)
    # x, y = findMax_2x2(pts_L_fund)
    # print(x, y)
    # ------------------------------------------- #

    for index in pts_inlier:  # for each index in pts_inlier
        i_L = index[1]  # take the i coord
        j_L = index[0]  # take the j coord
        # print(i_L)
        # print(j_L)
        col_r = red[i_L][j_L]  # find the red pixel color
        col_g = green[i_L][j_L]  # find the green pixel color
        col_b = blue[i_L][j_L]  # find the blue pixel color
        col = [col_r, col_g, col_b]  # store them to list named col
        colors.append(col)  # append the col list to color list
    return colors
