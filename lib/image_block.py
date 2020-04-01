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
        self.colors = []
        self.is_good = False

    def set_match(self, m_id: int, imgL_id: int, imgR_id: int, g_matches: [], g_matches_L: [], g_matches_R: [],
                  g_matches_id_L: [], g_matches_id_R: [], colors: [], is_good: bool):
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

    def create_index_table(self):
        index_tab = []
        for id_index in range(0, len(self.f_pts_indexes_L)):
            index_tab_tmp = []
            id_L = self.f_pts_indexes_L[id_index]
            id_R = self.f_pts_indexes_R[id_index]
            index_tab_tmp.append(id_L)
            index_tab_tmp.append(id_R)
            index_tab.append(index_tab_tmp)
        index_tab = np.array(index_tab)
        return index_tab

    def export_id_csv(self, path: str):
        id_list = []
        for i in range(0, len(self.f_pts_indexes_L)):
            tmp = []
            tmp.append(int(self.f_pts_indexes_L[i]))
            tmp.append(int(self.f_pts_indexes_R[i]))
            id_list.append(tmp)
        # print(id_list)
        np.savetxt(path, id_list, delimiter=",", fmt='%d')


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
