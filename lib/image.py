import os
import cv2
from lib.message_handling import *
from lib.camera import *

IMG_SIFT = "SIFT"
IMG_SURF = "SURF"
IMG_ORB = "ORB"
IMG_AKAZE = "AKAZE"


class ImageInfo:
    def __init__(self):
        self.id = 0
        self.src = ""
        self.dir = ""
        self.dir_name = ""
        self.name = ""
        self.suffix = ""
        self.width = 0
        self.height = 0
        self.color_bands = 1

    def set_image_id(self, index_id):
        self.id = index_id

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
        print("id:", self.id)
        print("full path:", self.src)
        print("directory:", self.dir)
        print("name:", self.name)
        print("suffix:", self.suffix)
        print("width:", self.width)
        print("height:", self.height)
        print("color bands:", self.color_bands)


class FeaturePoints:
    def __init__(self):
        self.exist = False
        self.kp_ids = []
        self.keypoints = []
        self.descriptors = []

    def set_feature_point_list(self, kp: [], descr: []):
        self.exist = True
        self.keypoints = kp
        self.descriptors = descr
        for i in range(0, len(self.keypoints)):
            self.kp_ids.append(i)


class PoseMatrix:
    R: []
    t: []

    T_mtrx: []

    def set_starting_pose_matrix(self):
        T = [[1.0, 0.0, 0.0, 0.0],
             [0.0, 1.0, 0.0, 0.0],
             [0.0, 0.0, 1.0, 0.0],
             [0.0, 0.0, 0.0, 1.0]]
        self.T_mtrx = np.array(T)

    def take_R_and_t(self):
        R = self.T_mtrx[:3, :3]
        t = self.T_mtrx[:3, 3:]
        return R, t

    def setPoseMatrix_R_t(self, R, t):
        Rt = []
        Rt.append(R)
        Rt.append(t)
        Rt = np.concatenate(Rt, axis=1)

        poseMtrx = []
        poseMtrx.append(Rt)
        poseMtrx.append([[0.0, 0.0, 0.0, 1.0]])
        poseMtrx = np.concatenate(poseMtrx, axis=0)

        self.T_mtrx = np.array(poseMtrx)

    def set_pose_mtrx_using_pair(self, pair_pose_mtrx):
        # print(pair_pose_mtrx)  # Uncomment for debugging
        # print(self.T_mtrx)  # Uncomment for debugging
        p_mtrx = np.dot(pair_pose_mtrx, self.T_mtrx)
        self.T_mtrx = np.array(p_mtrx)


class ProjectionMatrix:
    P_mtrx = []

    def set_starting_projection_matrix(self, cam_mtrx):
        projectionMtrx = []
        zeroMtrx = [[0], [0], [0]]
        projectionMtrx.append(cam_mtrx)
        projectionMtrx.append(zeroMtrx)
        projectionMtrx = np.concatenate(projectionMtrx, axis=1)
        self.P_mtrx = np.array(projectionMtrx)

    def set_projection_matrix_from_pose(self, R, t, cam_mtrx):
        R_t = np.transpose(R)
        m_R_t_t = np.dot(-R_t, t)

        P_tmp = []
        P_tmp.append(R_t)
        P_tmp.append(m_R_t_t)
        P_tmp = np.concatenate(P_tmp, axis=1)
        # print(P_tmp)

        P = np.dot(cam_mtrx, P_tmp)
        # print(P)
        self.P_mtrx = P


class Image:
    def __init__(self):
        self.info = ImageInfo()
        self.camera = Camera()
        self.feature_points = FeaturePoints()

        self.T_mtrx = PoseMatrix()  # Pose matrix for the current image
        self.P_mtrx = ProjectionMatrix()  # Projection matrix  for the current image

    def img_set_image_id(self, index_id):
        self.info.set_image_id(index_id)

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

    def img_get_img_rgb(self):
        img = cv2.imread(self.info.src)
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img
        return None

    def img_get_img_rgb_with_feature_points(self):
        img = cv2.imread(self.info.src)
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cv2.drawKeypoints(img, self.feature_points.keypoints, img)
            return img
        return None

    def img_find_feature_points(self, flag):
        if flag == IMG_SIFT:
            method = cv2.xfeatures2d_SIFT.create()
        elif flag == IMG_SURF:
            method = cv2.xfeatures2d_SURF.create()
        elif flag == IMG_ORB:
            method = cv2.ORB_create()
        elif flag == IMG_AKAZE:
            method = cv2.AKAZE_create()
        else:
            method = cv2.ORB_create()

        img = cv2.imread(self.info.src, cv2.IMREAD_GRAYSCALE)
        kp, descr = method.detectAndCompute(img, None)  # detect and compute keypoints
        self.feature_points.set_feature_point_list(kp, descr)

    def img_set_starting_pose_matrix(self, pose_mtrx: PoseMatrix):
        self.T_mtrx = pose_mtrx

    def img_set_starting_projection_matrix(self, proj_mtrx: ProjectionMatrix):
        self.P_mtrx = proj_mtrx