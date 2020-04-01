from lib.image import *


class ImageMatches:
    def __init__(self):
        self.match_id = int
        self.img_L_id = int
        self.img_R_id = int
        self.f_pts = []
        self.f_pts_L = []
        self.f_pts_R = []
        self.f_pts_indexes_L = []
        self.f_pts_indexes_R = []
        self.f_index_tab = []
        self.colors = []
        self.is_good = False

    def set_match(self, m_id: int, imgL_id: int, imgR_id: int, g_matches: [], g_matches_L: [], g_matches_R: [],
                  g_matches_id_L: [], g_matches_id_R: [], colors: [], is_good: bool):
        """
        Set the matching parameters
        :param m_id: Match id. Use this as reference to the matching pair.
        :param imgL_id: The id of the left image
        :param imgR_id: The id of the right image
        :param g_matches: The good match point list
        :param g_matches_L: The good match point list for left image
        :param g_matches_R: The good match point list for right image
        :param g_matches_id_L: The ids of the good points for the left image
        :param g_matches_id_R: The ids of the good points for the right image
        :param colors: The color of the points (take it from the left image)
        :param is_good: True/False depends for the number of good points
        :return: Nothing
        """
        self.match_id = m_id
        self.img_L_id = imgL_id
        self.img_R_id = imgR_id
        self.f_pts = g_matches
        self.f_pts_L = g_matches_L
        self.f_pts_R = g_matches_R
        self.f_pts_indexes_L = g_matches_id_L
        self.f_pts_indexes_R = g_matches_id_R
        self.colors = colors
        self.is_good = is_good
        self.create_index_table()

    def create_index_table(self):
        """
        Create an index table with the id list of images.
        :return: Nothing
        """
        for id_index in range(0, len(self.f_pts_indexes_L)):
            index_tab_tmp = []
            id_L = self.f_pts_indexes_L[id_index]
            id_R = self.f_pts_indexes_R[id_index]
            index_tab_tmp.append(id_L)
            index_tab_tmp.append(id_R)
            self.f_index_tab.append(index_tab_tmp)
        self.f_index_tab = np.array(self.f_index_tab)

    def export_id_csv(self, path: str):
        """
        Export id list as csv file (for debugging)
        :param path: the path to the exported file.
        :return: Nothing
        """
        id_list = []
        for i in range(0, len(self.f_pts_indexes_L)):
            tmp = []
            tmp.append(int(self.f_pts_indexes_L[i]))
            tmp.append(int(self.f_pts_indexes_R[i]))
            id_list.append(tmp)
        # print(id_list)
        np.savetxt(path, id_list, delimiter=",", fmt='%d')

    def INDEX_TABLE(self):
        """
        Return index table
        :return: self.f_index_tab
        """
        return self.f_index_tab

class ImageBlock:
    def __init__(self):
        self.img_list = []

    def b_img_create_image_list(self, img_list):
        """
        Create the image list.
        :param img_list:
        :return:
        """
        self.img_list = img_list

    def b_img_append_image_to_list(self, img: Image()):
        """
        Append an image to image list.
        :param img: Image()
        :return: Nothing
        """
        self.img_list.append(img)

    def b_img_match_all_images(self):
        """
        Match all images in block
        :return: Nothing
        """
        pass

    def b_img_fast_matching(self):
        """
        Match only consecutively images.
        :return: Nothing
        """
        pass
