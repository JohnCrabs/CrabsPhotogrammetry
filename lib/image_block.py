from lib.image import *
from lib.global_functions import *
from lib.point import *
from lib.color import *

LOWE_RATIO = 0.9
INLIER_RATIO = 0.3
POSE_RATIO = 0.05


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


class Landmark:
    l_id: int
    pnt3d: Point3d_float()
    color: ColorRGB()
    seen = 0

    match_id_list = []

    def set_landmark(self, l_id: int, x: float, y: float, z: float, seen: int, r=0, g=0, b=0):
        self.l_id = l_id
        pnt = Point3d_float()
        pnt.set_point(x, y, z)
        self.pnt3d = pnt
        col = ColorRGB()
        col.set_color(r, g, b)
        self.color = col
        self.seen = seen

    def append_pnt3d(self, pnt: Point3d_float):
        self.pnt3d.x += pnt.x
        self.pnt3d.y += pnt.y
        self.pnt3d.z += pnt.z
        self.seen += 1

    def finalize_coordinates(self):
        self.pnt3d.x /= self.seen
        self.pnt3d.y /= self.seen
        self.pnt3d.z /= self.seen

    def set_match_id_list(self, img_index_L, img_index_R):
        id_list = []
        id_list.append(img_index_L)
        id_list.append(img_index_R)
        self.match_id_list = id_list


class PairModel:
    id = 0
    imgL_id = 0
    imgR_id = 0
    imgL_name: str
    imgR_name: str
    points = []
    colors = []
    id_L_R_list = []
    Xo = 0
    Yo = 0
    Zo = 0

    inlier_L = []
    inlier_R = []
    inlier_id_L = []
    inlier_id_R = []
    camera = Camera()

    def set_model(self, index: int, imgL_id: int, imgR_id: int, id_list: [], points: [], colors: []):
        self.id = index
        self.imgL_id = imgL_id
        self.imgR_id = imgR_id
        self.id_L_R_list = id_list
        self.points = points
        self.colors = colors

    def set_model_img_names(self, imgL_name: str, imgR_name: str):
        self.imgL_name = imgL_name
        self.imgR_name = imgR_name

    def find_index_with_R_id(self, r_id: int):
        for index in range(0, len(self.id_L_R_list)):
            if r_id == self.id_L_R_list[index][1]:
                return index
        return -1

    def set_axis_origin(self, Xo: float, Yo: float, Zo: float):
        self.Xo = Xo
        self.Yo = Yo
        self.Zo = Zo

    def move_cloud_to_new_origin(self, Xo_new: float, Yo_new: float, Zo_new: float):
        dx = Xo_new - self.Xo
        dy = Yo_new - self.Yo
        dz = Zo_new - self.Zo

        self.Xo += dx
        self.Yo += dy
        self.Zo += dz

        for i in range(0, len(self.points)):
            self.points[i][0] += dx
            self.points[i][1] += dy
            self.points[i][2] += dz

    def scale_model(self, scale_factor: float):
        old_xo = self.Xo
        old_yo = self.Yo
        old_zo = self.Zo

        new_xo = 0.0
        new_yo = 0.0
        new_zo = 0.0
        point_size = len(self.points)

        for i in range(0, point_size):
            self.points[i][0] *= scale_factor
            self.points[i][1] *= scale_factor
            self.points[i][2] *= scale_factor

            new_xo += self.points[i][0]
            new_yo += self.points[i][1]
            new_zo += self.points[i][2]

        self.Xo = new_xo / point_size
        self.Yo = new_yo / point_size
        self.Zo = new_zo / point_size

        self.move_cloud_to_new_origin(old_xo, old_yo, old_zo)

    def rotate_translate_model(self, R: [], t: []):
        A = np.transpose(self.points)
        m, n = A.shape
        B2 = np.dot(R, A) + np.tile(t, (1, n))
        self.points = np.transpose(B2)


class BlockModel:
    landmark_ids = []
    landmark_shown = []
    landmark = []
    landmark_colors = []

    def create_landmark_model(self, pair_model_list: [], table_id_list: []):
        print("")
        print_message("Create Model from Pair Models.")

        # Find the Number of feature matching
        pairSize = 0
        model_size = len(pair_model_list)
        for i in range(1, model_size):
            pairSize += model_size - i

        pairCounter = 1
        landmarkCounter = 0
        pair_model_list_size = len(pair_model_list)
        for m_index_L in range(0, pair_model_list_size - 1):
            pm_L = pair_model_list[m_index_L]
            for m_index_R in range(m_index_L + 1, pair_model_list_size):
                pm_R = pair_model_list[m_index_R]

                pm_L_img_L_id = pm_L.imgL_id
                pm_L_img_R_id = pm_L.imgR_id
                pm_R_img_L_id = pm_R.imgL_id
                pm_R_img_R_id = pm_R.imgR_id

                img_L_L_name = pm_L.imgL_name
                img_L_R_name = pm_L.imgR_name
                img_R_L_name = pm_R.imgL_name
                img_R_R_name = pm_R.imgR_name

                print("")
                message = "( %d / " % pairCounter + "%d )" % pairSize
                print_message(message)
                message = "Find transformation parameters for " + "(" + img_L_L_name + "-" + img_L_R_name + ")" + \
                          "(" + img_R_L_name + "-" + img_R_R_name + ")"
                print_message(message)

                pm_id_list_tmp = []

                if pm_L_img_L_id == pm_R_img_L_id:
                    for l_id in range(0, len(table_id_list[pm_L_img_L_id])):
                        pm_L_id = table_id_list[pm_L_img_L_id][l_id][pm_L_img_R_id - pm_L_img_L_id]
                        pm_R_id = table_id_list[pm_L_img_L_id][l_id][pm_R_img_R_id - pm_R_img_L_id]
                        if pm_L_id != -1 and pm_R_id != -1:
                            pm_L_pnt_index = pm_L.find_index_with_R_id(pm_L_id)
                            pm_R_pnt_index = pm_R.find_index_with_R_id(pm_R_id)
                            if pm_L_pnt_index != -1 and pm_R_pnt_index != -1:
                                tmp = []
                                tmp.append(pm_L_pnt_index)
                                tmp.append(pm_R_pnt_index)
                                pm_id_list_tmp.append(tmp)
                                # print(pm_L_pnt_index, pm_L_id, pm_R_pnt_index, pm_R_id)
                elif pm_L_img_R_id == pm_R_img_L_id:
                    for l_id in range(0, len(table_id_list[pm_L_img_L_id])):
                        pm_L_id_r = table_id_list[pm_L_img_L_id][l_id][pm_L_img_R_id - pm_L_img_L_id]
                        if pm_L_id_r != -1:
                            for r_id in range(0, len(table_id_list[pm_R_img_L_id])):
                                pm_R_id_l = table_id_list[pm_R_img_L_id][r_id][0]
                                if pm_L_id_r == pm_R_id_l:
                                    pm_L_id = table_id_list[pm_L_img_L_id][l_id][pm_L_img_R_id - pm_L_img_L_id]
                                    pm_R_id = table_id_list[pm_R_img_L_id][r_id][pm_R_img_R_id - pm_R_img_L_id]
                                    if pm_L_id != -1 and pm_R_id != -1:
                                        pm_L_pnt_index = pm_L.find_index_with_R_id(pm_L_id)
                                        pm_R_pnt_index = pm_R.find_index_with_R_id(pm_R_id)
                                        if pm_L_pnt_index != -1 and pm_R_pnt_index != -1:
                                            tmp = []
                                            tmp.append(pm_L_pnt_index)
                                            tmp.append(pm_R_pnt_index)
                                            pm_id_list_tmp.append(tmp)
                                        # print(pm_L_pnt_index, pm_L_id, pm_R_pnt_index, pm_R_id)
                else:
                    print_message("Cannot match pairs without same images.")
                    break

                # print(debugging_test)
                # print(len(pm_id_list_tmp))
                # print(pm_id_list_tmp)
                points_src = []
                points_dst = []
                points_src_ids = []
                points_dst_ids = []
                for p_id in range(0, len(pm_id_list_tmp)):
                    id_l = pm_id_list_tmp[p_id][0]
                    id_r = pm_id_list_tmp[p_id][1]

                    pnt_l = pm_L.points[id_l]
                    pnt_l = [pnt_l[0], pnt_l[1], pnt_l[2]]
                    pnt_r = pm_R.points[id_r]
                    pnt_r = [pnt_r[0], pnt_r[1], pnt_r[2]]

                    points_src.append(pnt_l)
                    points_dst.append(pnt_r)
                    points_src_ids.append(id_l)
                    points_dst_ids.append(id_r)

                print_message("Found %d" % len(points_src) + " cloud matching points.")
                if len(points_src) > 10:
                    print_message("Calculate scale.")
                    scale, scale_error = find_scale_parameter(points_src, points_dst)
                    print("Scale = ", scale)
                    print("Scale_error = ", scale_error)

                else:
                    print_message("Too few matching points. Cannot match these pairs")
                    break

                print_message("Scale model " + img_R_L_name + "-" + img_R_R_name)

                pm_R.scale_model(scale)
                exp_points = pm_R.points
                exp_colors = pm_R.colors
                if exportCloud != "":
                    exportName = exportCloud + img_R_L_name + "_" + img_R_R_name + "_scale.ply"
                    message = "Export Scale Pair Model as : " + exportName
                    print_message(message)
                    export_as_ply(exp_points, exp_colors, exportName)

                points_dst = []
                for i in range(0, len(points_src)):
                    id_r = pm_id_list_tmp[i][1]
                    points_dst.append(exp_points[id_r])

                points_src = np.array(points_src)
                points_dst = np.array(points_dst)

                # print(len(points_src))
                # print(len(points_dst))

                # print(points_src)
                points_src_t = points_src.T
                points_dst_t = points_dst.T

                R, t = rigid_transform_3D(points_dst_t, points_src_t)

                print("")
                print_message("Rotation Mtrx = ")
                print(R)
                print("")
                print_message("Translation Mtrx = ")
                print(t)
                pm_R.rotate_translate_model(R, t)
                exp_points = pm_R.points
                exp_colors = pm_R.colors
                if exportCloud != "":
                    exportName = exportCloud + "finalβλέ/" + img_R_L_name + "_" + img_R_R_name + "_R_t.ply"
                    message = "Export Rotate + Translate Pair Model as : " + exportName
                    print_message(message)
                    export_as_ply(exp_points, exp_colors, exportName)

                if landmarkCounter == 0:
                    self.landmark = exp_points
                    self.landmark_colors = exp_colors
                    for i in range(0, len(self.landmark)):
                        self.landmark_shown.append(1)

                    landmarkCounter += 1

                else:
                    pass

                pairCounter += 1


class ImageBlock:
    def __init__(self):
        self.img_list = []

        self.img_matches = []  # A list of ImageMatches class items (store all matching information)
        self.block_match_list = []  # A list which contains all id matches

        self.pair_model = []  # A list or PairModel class items (store all early point clouds)
        self.block_model = BlockModel()  # Create a block model item

    # *** IMAGE LIST *** #
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

    # *** MATCH IMAGES *** #

    def b_img_append_matches(self, image_matches: ImageMatches()):
        """
        Append an ImageMatches object to image_matches list
        :param image_matches: ImageMatches() object
        :return: Nothing
        """
        self.matches.append(image_matches)

    def b_img_find_the_number_of_matches_fast(self):
        # Find the Number of feature matching
        matchSize = 0  # set a matchSize counter
        block_size = len(self.img_list)  # blockSize = number of images
        for i in range(1, block_size):  # for i in range(1, block_size) => matchSize = Sum_{i=1}^{N}(matchSize+i)
            matchSize += 1  # perform the previous equation
        return matchSize  # return matchSize

    def b_img_find_the_number_of_matches_all_images(self):
        # Find the Number of feature matching
        matchSize = 0  # set a matchSize counter
        block_size = len(self.img_list)  # blockSize = number of images
        for i in range(1, block_size):  # for i in range(1, block_size) => matchSize = Sum_{i=1}^{N}(blockSize - i)
            matchSize += block_size - i  # perform the previous equation
        return matchSize  # return matchSize

    def b_img_match_pairs(self, matcher, imgL_index: int, imgR_index: int, matchCounter: int, matchSize: int):
        """
        Match the feature points of a pair of images.
        :param matcher: The cv2 matcher
        :param imgL_index: the index of the left image
        :param imgR_index: the index of the right image
        :param matchCounter: the matching id
        :param matchSize: the size of the matches needs to perform (for console debugging)
        :return: Nothing
        """
        img_L = self.img_list[imgL_index]  # create a copy of the left image (for code readability)
        img_R = self.img_list[imgR_index]  # create a copy of the right image (for code readability)

        # Debugging message lines
        print("")
        message = "Match %d" % matchCounter + " out of " + "%d matches needed to perform." % matchSize
        message_print(message)

        img_L_name = img_L.info.name  # Take the name of the left image
        img_R_name = img_R.info.name  # Take the name of the right image

        # Debugging message lines
        message = "Match images %s" % img_L_name + " and " + "%s" % img_R_name
        message_print(message)

        kp_L = img_L.feature_points.keypoints  # Take the keypoints of left image
        kp_R = img_R.feature_points.keypoints  # Take the keypoints of right image

        desc_L = img_L.feature_points.descriptors  # Take the descriptors of left image
        desc_R = img_R.feature_points.descriptors  # Take the descriptors of right image

        kp_id_list_L = img_L.feature_points.kp_ids  # Take the kp_ids of left image
        kp_id_list_R = img_R.feature_points.kp_ids  # Take the kp_ids of right image

        matched_points = matcher.knnMatch(desc_L, desc_R, k=2)  # Mach Images

        # Find all good points as per Lower's ratio.
        good_matches = []  # list for good matches
        points_L_img = []  # list for the points coords in the left image
        points_R_img = []  # list for the points coords in the right image
        points_L_img_ids = []  # list for the ids of the left image
        points_R_img_ids = []  # list for the ids of the right image
        match_pnt_size = 0  # counter for the match point size
        for m, n in matched_points:
            match_pnt_size += 1  # increase the counter (this counter is used for console debugging)
            if m.distance < LOWE_RATIO * n.distance:
                good_matches.append(m)
                points_L_img.append(kp_L[m.queryIdx].pt)  # Take p_coords for left img
                points_R_img.append(kp_R[m.trainIdx].pt)  # Take p_coords for right img

                points_L_img_ids.append(kp_id_list_L[m.queryIdx])  # Take the ids for the left image
                points_R_img_ids.append(kp_id_list_R[m.trainIdx])  # Take the ids for the right image
        g_pnts_size = len(good_matches)  # take the size of good matches

        # Debugging message lines
        message = "Found %d" % g_pnts_size + " good matches out of %d" % match_pnt_size + " matching points."
        message_print(message)

        # Create numpy arrays
        good_matches = np.array(good_matches)  # ALL GOOD MATCHES
        points_L_img = np.array(points_L_img)  # POINTS_L
        points_R_img = np.array(points_R_img)  # POINTS_R
        points_L_img_ids = np.array(points_L_img_ids)  # ID_L
        points_R_img_ids = np.array(points_R_img_ids)  # ID_R

        # print(points_L_img_ids)  # uncomment for console debugging
        # print(points_R_img_ids)  # uncomment for console debugging
        # Calculate inliers using Fundamental Matrix
        # Debugging message line
        message_print("Calculate inlier matches.")

        pts_L_fund = np.int32(points_L_img)  # Transform float to int32
        pts_R_fund = np.int32(points_R_img)  # Transform float to int32

        F, mask = cv2.findFundamentalMat(pts_L_fund, pts_R_fund)  # Find fundamental matrix using RANSARC
        # We select only inlier points
        pts_inlier_matches = good_matches[mask.ravel() == 1]  # Select inliers for good matches
        pts_inlier_L = points_L_img[mask.ravel() == 1]  # Select inliers from imgL using fundamental mask
        pts_inlier_R = points_R_img[mask.ravel() == 1]  # Select inliers from imgR using fundamental mask
        pts_inlier_L_ids = points_L_img_ids[mask.ravel() == 1]  # Select inlier IDS from imgL_index
        # using fundamental mask
        pts_inlier_R_ids = points_R_img_ids[mask.ravel() == 1]  # Select inliers IDS from imgR_index
        # using fundamental mask

        # Calculate the Color of an Image
        pts_L_fund = pts_L_fund[mask.ravel() == 1]  # find the pixels of fundamental points
        color_inlier_L = find_color_list(img_L, pts_L_fund)  # find the corresponding color on left image
        color_inlier_R = find_color_list(img_R, pts_R_fund)  # find the corresponding color on right image

        # This may not be the best way to pick the color of the points in point cloud, but its a fair way.
        # It may be better to pick color either from left or right image.
        color_inlier = []  # create color inlier list
        for i in range(0, len(color_inlier_L)):  # for i in range(0,color_inlier_L_size)
            col_r = (int(color_inlier_L[i][0]) + int(color_inlier_R[i][0])) / 2  # find the average red
            col_g = (int(color_inlier_L[i][1]) + int(color_inlier_R[i][1])) / 2  # find the average green
            col_b = (int(color_inlier_L[i][2]) + int(color_inlier_R[i][2])) / 2  # find the average blue
            color = [int(col_r), int(col_g), int(col_b)]  # store them to color list
            color_inlier.append(color)  # append color to color inlier list
        # print(color_inlier)  # Uncomment for console debugging

        match_tmp = ImageMatches()  # Create a temporary match item
        # match_tmp.set_match(m_id=matchCounter-1, imgL_id=img_L.id, imgR_id=img_R.id, g_matches=good_matches,
        #                    g_matches_L=points_L_img, g_matches_R=points_R_img,
        #                    g_matches_id_L=points_L_img_ids, g_matches_id_R=points_R_img_ids)

        g_pnt_size = len(good_matches)  # Find the size of q_pnts
        inliers_size = len(pts_inlier_L_ids)  # Find the size of inliers

        # Check if the image matching is good (this ratio is mine and arise from the thought that in 100 points
        # we need to have at least 100*INLIER_RATIO for a good mach pair)
        match_is_good = True
        if inliers_size < INLIER_RATIO * g_pnts_size:
            match_is_good = False

        match_tmp.set_match(m_id=matchCounter - 1, imgL_id=img_L.info.id, imgR_id=img_R.info.id,
                            g_matches=pts_inlier_matches, g_matches_L=pts_inlier_L, g_matches_R=pts_inlier_R,
                            g_matches_id_L=pts_inlier_L_ids, g_matches_id_R=pts_inlier_R_ids,
                            colors=color_inlier, is_good=match_is_good)

        # Print the sizes to screen so we can see the difference.
        # In every step we need to exclude unfitting points for creating better results.
        message = "Found %d" % inliers_size + " inlier matches out of %d" % g_pnt_size + \
                  " good feature matching points."
        message_print(message)
        self.img_matches.append(match_tmp)

    def b_img_match_all_images(self):
        """
        Match all images in block
        :return: Nothing
        """
        # Create matcher
        matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)

        matchSize = self.b_img_find_the_number_of_matches_all_images()

        message_print("Needs to perform %d matches." % matchSize)

        # Create matches
        matchCounter = 1
        block_size = len(self.img_list)
        for imgL_index in range(0, block_size - 1):
            for imgR_index in range(imgL_index + 1, block_size):
                self.b_img_match_pairs(matcher, imgL_index, imgL_index + 1, matchCounter, matchSize)
                matchCounter += 1  # increase the matchCounter
        self.b_img_create_block_match_list()

    def b_img_fast_matching(self):
        """
        Match only consecutively images.
        :return: Nothing
        """
        # Create matcher
        matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)

        matchSize = self.b_img_find_the_number_of_matches_fast()

        message_print("Needs to perform %d matches." % matchSize)

        # Create matches
        matchCounter = 1
        block_size = len(self.img_list)
        for imgL_index in range(0, block_size - 1):
            self.b_img_match_pairs(matcher, imgL_index, imgL_index + 1, matchCounter, matchSize)
            matchCounter += 1  # increase the matchCounter
        self.b_img_create_block_match_list()

    def b_img_create_block_match_list(self):
        block_match_list_tmp = []  # create block image list

        for img_id in range(0, len(self.img_list) - 1):  # for img_id in range(0, img_list_size -1 )
            img = self.img_list[img_id]  # copy img from img list
            kp_ids = img.feature_points.keypoints  # copy key points id

            match_list_tmp = []  # create match list tmp
            for i in range(0, len(kp_ids)):  # for all keypoints id
                tmp = [i]  # set i to tmp list
                for j in range(img.info.id + 1, len(self.img_list)):  # for all images
                    tmp.append(-1)  # append -1 (value that indicates no match)
                match_list_tmp.append(tmp)  # append it to match_list_tmp
            # print(match_list_tmp)
            block_match_list_tmp.append(match_list_tmp)  # append it to block match tmp

        for m in self.img_matches:  # for all img matches
            imgL_id = m.img_L_id  # take the left image matching id
            imgR_id = m.img_R_id  # take the right image matching id
            # print(imgL_id, imgR_id)
            # print(block_match_list_tmp[imgL_id])
            match_ids_L = m.f_pts_indexes_L  # take the feature points ids for left image
            match_ids_R = m.f_pts_indexes_R  # take the feature points ids for right image
            for index in range(0, len(match_ids_L)):  # for all matches
                block_match_list_tmp[imgL_id][match_ids_L[index]][imgR_id - imgL_id] = match_ids_R[index]  # set table
            # print(block_match_list_tmp[imgL_id])
        self.block_match_list = block_match_list_tmp  # save it to block match list
        # print(self.block_match_list)  # print list for debugging

    def b_img_transform_landmark_to_list_items(self, landmark: []):
        points = []
        colors = []
        id_list = []
        for l_pnt in landmark:
            x = l_pnt.pnt3d.x
            y = l_pnt.pnt3d.y
            z = l_pnt.pnt3d.z
            r = l_pnt.color.r
            g = l_pnt.color.g
            b = l_pnt.color.b
            pt_tmp = [x, y, z]
            # col = [0, 0, 0]
            col = [r, g, b]
            # print(col)
            points.append(pt_tmp)
            colors.append(col)
            id_list.append(l_pnt.match_id_list)
            # print(pt_tmp)
        points = np.array(points)
        colors = np.array(colors)
        id_list = np.array(id_list)
        return points, colors, id_list

    def b_img_create_pair_models(self):
        print("")
        message_print("Find Landmarks")

        matchSize = len(self.img_matches)  # take the size of the matches
        # print(matchSize) # Uncomment for debugging

        # Landmark Founder
        matchCounter = 1  # set match counter to one (1)
        set_start_mtrx = True  # set start matrix boolean to True
        landmarkCounter = 0  # set landmark Counter to zero (0)
        pairModelCounter = 0  # set pair model counter to zero (0)
        for match in self.img_matches:  # for each matching pair
            imgL_index = match.img_L_id  # read left img id
            imgR_index = match.img_R_id  # read right img id

            imgL = self.img_list[imgL_index]  # read left img (we need it for the index key table)
            imgR = self.img_list[imgR_index]  # read right img (we need it for general information like name)
            # print(imgR)

            imgL_name = imgL.info.name  # read left img name
            imgR_name = imgR.info.name  # read right img name

            pts_inlier_L = match.f_pts_L  # read good matching points left
            pts_inlier_R = match.f_pts_R  # read good matching points right

            pts_inlier_L_id = match.f_pts_indexes_L  # read good matching points left indexes
            pts_inlier_R_id = match.f_pts_indexes_R  # read good matching points right indexes

            colors = match.colors  # take the colors

            # Debugging message lines
            print("")
            message = "(%d / " % matchCounter + "%d)" % matchSize
            message_print(message)
            message = "Find landmark in images %s" % imgL_name + " and %s." % imgR_name
            message_print(message)

            # I prefer inlier solution.
            cam_mtrx = imgL.camera.mtrx  # i assume the two images have same camera mtrx
            E, mask = cv2.findEssentialMat(pts_inlier_L, pts_inlier_R, cam_mtrx)  # Find essential matrix
            # print(E)

            # Calculate pose matrix R and t
            # poseVal = The number of pose points (we'll use these points to create the cloud)
            #    R    = Rotate Matrix
            #    t    = Translate Matrix
            #  mask   = Take values 0 and 1 and if 1 this point is pose point (object point)
            poseVal, R, t, mask = cv2.recoverPose(E, pts_inlier_L, pts_inlier_R, cam_mtrx)  # find R and t matrices
            poseMask = mask  # Keep the mask in a variable poseMask (I done this for easier code reading)

            # The poseVal value indicates the candidate number of new object points.
            # I named it candidate because some of these points may be visible from previous images.
            # In this case we need to find the average of these points. This method remove dublicate points and
            # increase the accuracy of the final point cloud.
            g_p_size = len(pts_inlier_L_id)  # take the size of pts_inlier_L_id = pts_inlier_R_id
            # Debugging message lines
            message = "Found %d" % poseVal + " candidate object points out %d suggested matching points." % g_p_size
            message_print(message)

            if set_start_mtrx:  # if we are in the first loop
                set_start_mtrx = False  # set star matrix boolean to False
                pose_mtrx_img_0 = PoseMatrix()  # create PoseMatrix object
                pose_mtrx_img_0.set_starting_pose_matrix()  # set starting pose matrix
                imgL.img_set_starting_pose_matrix(pose_mtrx_img_0)  # set starting point matrix to imgL

                proj_mtrx_img_0 = ProjectionMatrix()  # create projection Matrix
                proj_mtrx_img_0.set_starting_projection_matrix(imgL.camera.mtrx)  # set starting projection matrix
                imgL.img_set_starting_projection_matrix(proj_mtrx_img_0)  # set starting projection matrix to imgL

            landmark_debugging_list = []  # Create landmark list (for debugging)
            if poseVal > POSE_RATIO * g_p_size and match.is_good:  # check if we have good match points
                # Create the pose matrices.
                # Create the Pose and Projection Matrices
                # Debugging message line
                message_print("Calculate Pose Matrices:")

                pose_mtrx_L_T = imgL.T_mtrx.T_mtrx  # take the pose matrix of the left image

                pose_mtrx_R = PoseMatrix()  # Create PoseMatrix object for the right image
                pose_mtrx_R.setPoseMatrix_R_t(R, t)  # Set pose matrix using R, t values (taken from Essential Matrix)
                pose_mtrx_R.set_pose_mtrx_using_pair(pose_mtrx_L_T)  # Finalize pose matrix using the T_mtrx_L

                proj_mtrx_L_P = imgL.P_mtrx.P_mtrx  # take the projection matrix of the left image

                R, t = pose_mtrx_R.take_R_and_t()  # Find the new R,t values of the right image (taken from pose matrix)
                proj_mtrx_R_P = ProjectionMatrix()  # Create projection matrix object
                proj_mtrx_R_P.set_projection_matrix_from_pose(R, t, imgR.camera.mtrx)  # Set the projection matrix

                if (imgR.info.id - imgL.info.id) == 1:  # Check if the images are sequential
                    imgR.img_set_starting_pose_matrix(pose_mtrx_R)  # Set the pose matrix to the right img
                    imgR.img_set_starting_projection_matrix(proj_mtrx_R_P)  # Set the projection matrix to the right img

                # print("")
                # print("pose_mtrx_L = \n", pose_mtrx_L_T)  # Uncomment for debug
                # print("")
                # print("pose_mtrx_R = \n", pose_mtrx_R.T_mtrx)  # Uncomment for debug
                # print("")
                # print("proj_mtrx_L = \n", proj_mtrx_L_P)  # Uncomment for debug
                # print("")
                # print("proj_mtrx_R = \n", proj_mtrx_R_P.P_mtrx)  # Uncomment for debug

                # Triangulate
                proj_mtrx_R_P = proj_mtrx_R_P.P_mtrx  # Change the object from ProjectionMatrix() to P_mtrx list

                # Debugging message line
                message_print("Triangulation.")

                triang_pnts_L = np.transpose(pts_inlier_L)  # Set triangulation points for Left image
                triang_pnts_R = np.transpose(pts_inlier_R)  # Set triangulation points for Right image

                # Triangulate points
                points4D = cv2.triangulatePoints(projMatr1=proj_mtrx_L_P,
                                                 projMatr2=proj_mtrx_R_P,
                                                 projPoints1=triang_pnts_L,
                                                 projPoints2=triang_pnts_R)
                # print(points4D)  # Uncomment for debugging

                # Find Good LandMark Points and Set Them to List
                # print(pts_inlier_L_id)
                # print(pts_inlier_R_id)
                for l_index in range(0, g_p_size):  # for all left indexes
                    if poseMask[l_index] != 0:  # check in poseMask for the good points
                        # print(poseMask[l_index]) # Uncomment for debugging
                        # print(l_index)  # Uncomment for debugging

                        pt3d = Point3d_float()  # Create a Point3d_float() object

                        # I chose to use this way rather than my build in set_point(x,y,z) function
                        # for code reading simplicity.
                        pt3d.x = points4D[0][l_index] / points4D[3][l_index]  # Set x value
                        pt3d.y = points4D[1][l_index] / points4D[3][l_index]  # Set y value
                        pt3d.z = points4D[2][l_index] / points4D[3][l_index]  # Set z value

                        # Find the color of the point
                        r = colors[l_index][0]  # Take the red value for this point
                        g = colors[l_index][1]  # Take the green value for this point
                        b = colors[l_index][2]  # Take the blue value for this point
                        # print(r, g, b)
                        # ---------------------------------------------------------------------------- #
                        l_pnt = Landmark()
                        l_pnt.set_landmark(landmarkCounter, pt3d.x, pt3d.y, pt3d.z, 1, r, g, b)
                        l_pnt.set_match_id_list(pts_inlier_L_id[l_index], pts_inlier_R_id[l_index])

                        landmark_debugging_list.append(l_pnt)
                        landmarkCounter += 1
                pair_model_tmp = PairModel()

                # Take the
                exp_points, exp_colors, exp_id = self.b_img_transform_landmark_to_list_items(landmark_debugging_list)

                # ---------------------------------------------------------------------------------------------- #
                # These lines are from another version. I leave them here for a quick debugging
                # ---------------------------------------------------------------------------------------------- #
                # exportName = exportPath + imgL_name + "_" + imgR_name + ".ply"
                # message = "Export Pair Model as : " + exportName
                # message_print(message)
                # export_as_ply(exp_points, exp_colors, exportName)
                # ---------------------------------------------------------------------------------------------- #
                pair_model_tmp.set_model(pairModelCounter, imgL.info.id, imgR.info.id,  exp_id, exp_points, exp_colors)
                self.pair_model.append(pair_model_tmp)
            else:
                # Debugging message line
                message = "Cannot create pair model from images " + imgL_name + " and " + imgR_name + \
                          ", due to few points."
                message_print(message)

                imgR.set_starting_pose_matrix(imgL.T_mtrx)  # Set left pose matrix as right pose matrix
                imgR.set_starting_projection_matrix(imgL.P_mtrx)  # Set L projection matrix as R projection matrix
            matchCounter += 1  # increase the matchCounter

    def b_img_create_block_model(self):
        self.block_model.create_landmark_model(self.pair_model, self.block_match_list)
