import sys
from ui_wins.mainwin import *
from ui_wins.video2images import *
from ui_wins.simple_image_viewer import *

from PyQt5.Qt import (Qt, QDialog, QDir, QFileDialog, QListWidgetItem, QMessageBox, QWidget, QLabel, QPixmap, QImage,
                      QSize, QCheckBox)

from lib.video import *
from lib.image import *
from lib.image_block import *


class Window:
    def __init__(self):
        # ---------------------------------------------------------------------------------------------------------- #
        # START OF APPLICATION
        # ------------------------
        # ------------------------
        # Set flags
        # ------------------------
        # *** SET AS SWITCH UP/DOWN *** #
        self.UP = True
        self.DOWN = False
        # *** IMAGES *** #
        self.ALL_IMG_FORMAT = "All Supported (*.jpg *.jpeg *.jpe *.png *.bmp *.tif *.tiff " \
                              "*.dib *.pbm *.pgm *.ppm *.sr *.ras)"
        self.JPG_FORMAT = "JPG (*.jpg *.jpeg *.jpe)"
        self.PNG_FORMAT = "PNG (*.png)"
        self.BMP_FORMAT = "BMP (*.bmp)"
        self.TIF_FORMAT = "TIFF (*.tif *.tiff)"
        self.DIB_FORMAT = "DIB (*.dib)"
        self.PBM_FORMAT = "PBM (*.pbm)"
        self.PGM_FORMAT = "PGM (*.pgm)"
        self.PPM_FORMAT = "PPM (*.ppm)"
        self.SR__FORMAT = "SR (*.sr)"
        self.RAS_FORMAT = "RAS (*.ras)"
        self.DD = ";;"
        self.IMG_FILTER = self.ALL_IMG_FORMAT + self.DD + self.JPG_FORMAT + self.DD + self.PNG_FORMAT + self.DD + \
                          self.BMP_FORMAT + self.DD + self.TIF_FORMAT + self.DD + self.DIB_FORMAT + self.DD + \
                          self.PBM_FORMAT + self.DD + self.PGM_FORMAT + self.DD + self.PPM_FORMAT + self.DD + \
                          self.SR__FORMAT + self.DD + self.RAS_FORMAT
        # *** VIDEOS *** #
        self.ALL_VID_FORMAT = "All Supported (*.mov *.MOV *.mp4 *.avi)"
        self.MOV_FORMAT = "MOV (*.mov *.MOV)"
        self.MP4_FORMAT = "MP4 (*.mp4)"
        self.AVI_FORMAT = "AVI (*.avi)"
        self.VID_FILTER = self.ALL_VID_FORMAT + self.DD + self.MOV_FORMAT + self.DD + self.MP4_FORMAT + self.DD\
                          + self.AVI_FORMAT
        # *** Qt FLAGS *** #
        self.DIALOG_FLAG = QFileDialog.DontUseNativeDialog
        self.Q_ASPECT_RATIO = Qt.KeepAspectRatio
        # *** FEATURE OPTION FLAG *** #
        self.F_SIFT = IMG_SIFT
        self.F_SURF = IMG_SURF
        self.F_ORB = IMG_ORB
        self.F_AKAZE = IMG_AKAZE
        # ------------------------
        # Flags Section ends here
        # ---------------------------------------------------------------------------------------------------------- #
        #
        # ------------------------
        # Set class items
        # ------------------------
        self.video_list = []
        self.image_list = []
        self.image_block = ImageBlock()

        self.img_view_index = 0
        self.draw_kp = self.DOWN
        # ------------------------
        # Class items ends here
        # ---------------------------------------------------------------------------------------------------------- #
        # ------------------------
        # Set up the ui
        # ------------------------
        # *** MAIN_UI *** #
        self.app = QtWidgets.QApplication(sys.argv)
        self.ui_main_win = Ui_MainWindow()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui_main_win.setupUi(self.MainWindow)

        # *** VIDEO TO IMAGES UI *** #
        self.ui_video2images = Ui_Video2Images()
        self.Video2Images = QDialog()
        self.ui_video2images.setupUi(self.Video2Images)

        # *** SIMPLE IMAGE VIEWER *** #
        self.ui_simple_img_viewer = Ui_SimpleImageViewer()
        self.SimpleImageViewer = QDialog()
        self.ui_simple_img_viewer.setupUi(self.SimpleImageViewer)

        # ------------------------
        # Setting up ends here
        # ---------------------------------------------------------------------------------------------------------- #
        # ------------------------
        # Actions list starts here
        # ------------------------
        # *** UI_MAIN_WIN *** #
        # ** FILE ** #
        self.ui_main_win.actionExit.triggered.connect(self.exit_window)  # actionExit
        # *** IMAGE *** #
        self.ui_main_win.actionImageImport.triggered.connect(self.image_import)  # actionImageImport
        self.ui_main_win.button_add_image.clicked.connect(self.image_import)  # button_add_image
        self.ui_main_win.button_del_image.clicked.connect(self.image_delete)  # button_del_image
        self.ui_main_win.actionImage_Viewer.triggered.connect(self.simgv_open)  # actionImage_Viewer

        self.ui_main_win.actionApproximate_Interior_Orientation.triggered.connect(self.image_approximate_camera)
        self.ui_main_win.actionSIFT.triggered.connect(lambda: self.image_find_feature_points(self.F_SIFT))
        self.ui_main_win.actionSURF.triggered.connect(lambda: self.image_find_feature_points(self.F_SURF))
        self.ui_main_win.actionORB.triggered.connect(lambda: self.image_find_feature_points(self.F_ORB))
        self.ui_main_win.actionAKAZE.triggered.connect(lambda: self.image_find_feature_points(self.F_AKAZE))
        self.ui_main_win.actionCreate_Block.triggered.connect(self.image_create_block)
        self.ui_main_win.actionAll_Images_Matching.triggered.connect(lambda: self.image_matching(fast=False))
        self.ui_main_win.actionFast_Matching.triggered.connect(lambda: self.image_matching(fast=True))

        # *** SIMPLE IMAGE VIEWER *** #
        self.ui_simple_img_viewer.button_previous.clicked.connect(self.simgv_button_previous)
        self.ui_simple_img_viewer.button_next.clicked.connect(self.simgv_button_next)
        self.ui_simple_img_viewer.check_box_draw_keypoints.stateChanged.connect(self.simgv_kp_view_check)

        # *** VIDEO *** #
        self.ui_main_win.actionVideoImport.triggered.connect(self.video_import)  # actionVideoImport
        self.ui_main_win.actionVideo_to_Images.triggered.connect(self.video2images)  # actionVideo_to_Images
        self.ui_main_win.button_add_video.clicked.connect(self.video_import)  # button_add_video
        self.ui_main_win.button_del_video.clicked.connect(self.video_delete)  # button_del_video

        # *** UI_VIDEO_2_IMAGES *** #
        self.ui_video2images.button_cancel.clicked.connect(self.video2images_cancel)
        self.ui_video2images.button_compute.clicked.connect(self.video2images_compute)
        self.ui_video2images.combo_box_select_video.currentTextChanged.connect(self.video2images_set_fps_for_video)
        self.ui_video2images.button_export_images_at.clicked.connect(self.video2images_set_export_folder)

        # ------------------------
        # Actions list ends here
        # ---------------------------------------------------------------------------------------------------------- #
        # ------------------------
        # Main loop and exit app
        # ------------------------
        self.MainWindow.show()
        sys.exit(self.app.exec_())
        # ------------------------
        # END OF APPLICATION
        # ---------------------------------------------------------------------------------------------------------- #

    # -------------------
    # ACTION FUNCTIONS
    # -------------------

    # *** FILE *** #

    def exit_window(self):
        """
        Signal exit application
        :return: Nothing
        """
        self.MainWindow.close()  # Close The window

    # *** IMAGES *** #

    def image_import(self):
        """
        Take the path(s) of one or more images and import them to the application.
        :return: Nothing
        """
        file_dialog = QFileDialog()
        f_path = file_dialog.getOpenFileNames(parent=None,
                                              caption="Open Image(s)",
                                              directory=QDir.homePath(),
                                              filter=self.IMG_FILTER,
                                              options=self.DIALOG_FLAG)[0]
        if f_path:
            img_id_counter = 0
            for file in f_path:
                image_tmp = Image()
                success = image_tmp.img_open(file)
                if success:
                    image_tmp.img_set_image_id(img_id_counter)
                    img_id_counter += 1
                    image_tmp.img_print_info()
                    self.image_list.append(image_tmp)
                    item_name = "../" + image_tmp.info.dir_name + "/" + image_tmp.info.name
                    item_widget = QListWidgetItem(item_name)
                    item_widget.setFlags(item_widget.flags() | QtCore.Qt.ItemIsUserCheckable)
                    item_widget.setCheckState(QtCore.Qt.Checked)
                    self.ui_main_win.listImage.addItem(item_widget)
                    self.ui_main_win.menuCamera_Settings.setEnabled(self.UP)

    def image_delete(self):
        """
        Delete an image from the list
        :return: Nothing
        """
        item_list = self.ui_main_win.listImage.selectedItems()
        if not item_list:
            return
        for item in item_list:
            self.image_list.pop(self.ui_main_win.listImage.row(item))
            self.ui_main_win.listImage.takeItem(self.ui_main_win.listImage.row(item))
        image_list_counter = 0
        for image in self.image_list:
            image.img_set_image_id(image_list_counter)
            image_list_counter += 1
        self.image_list_info()

    def image_list_info(self):
        for image in self.image_list:
            image.img_print_info()

    def image_default_approximate_camera_checked(self):
        self.ui_main_win.actionApproximate_Interior_Orientation.setChecked(self.DOWN)

    def image_approximate_camera(self):
        success = False
        for image in self.image_list:
            success = True
            image.img_approximate_camera_parameters()
            # image.img_print_camera_matrix()
        # self.image_list[0].img_print_camera_matrix()
        if success:
            self.ui_main_win.menuFind_Feature_Points.setEnabled(self.UP)
            self.ui_main_win.actionApproximate_Interior_Orientation.setChecked(self.UP)
            message_box_widget = QWidget()
            QMessageBox.information(message_box_widget, "Approximate Interior Orientation",
                                    "Process finished successfully!")

    def image_default_find_feature_points_checked(self):
        self.ui_main_win.actionSIFT.setChecked(self.DOWN)
        self.ui_main_win.actionSURF.setChecked(self.DOWN)
        self.ui_main_win.actionORB.setChecked(self.DOWN)
        self.ui_main_win.actionAKAZE.setChecked(self.DOWN)

    def image_find_feature_points(self, flag):
        success = False
        for image in self.image_list:
            success = True
            image.img_find_feature_points(flag=flag)
        if success:
            self.image_default_find_feature_points_checked()
            if flag == self.F_AKAZE:
                self.ui_main_win.actionAKAZE.setChecked(self.UP)
            elif flag == self.F_ORB:
                self.ui_main_win.actionORB.setChecked(self.UP)
            self.ui_simple_img_viewer.check_box_draw_keypoints.setEnabled(self.UP)
            self.ui_simple_img_viewer.check_box_draw_keypoints.setChecked(self.DOWN)
            self.draw_kp = self.DOWN
            self.ui_main_win.actionCreate_Block.setEnabled(self.UP)
            message_box_widget = QWidget()
            QMessageBox.information(message_box_widget, flag,
                                    "Process finished successfully!")

    def image_default_create_block_checked(self):
        pass

    def image_create_block(self):
        image_list_tmp = []
        image_list_size = len(self.image_list)
        success = False
        counter = 0
        for index_id in range(0, image_list_size):
            if self.ui_main_win.listImage.item(index_id).checkState():
                counter += 1
                if counter > 1:
                    success = True
                image_list_tmp.append(self.image_list[index_id])
        # print(image_list_tmp)
        if success:
            self.ui_main_win.actionCreate_Block.setChecked(self.UP)
            self.image_block.b_img_create_image_list(image_list_tmp)
            self.ui_main_win.menuImage_Matching.setEnabled(self.UP)
            message_box_widget = QWidget()
            QMessageBox.information(message_box_widget, "Create Block",
                                    "Process finished successfully!")

    def image_matching(self, fast=False):
        if fast:
            print("fast method")
        else:
            print("All Images")

    # *** SIMPLE IMAGE VIEWER (SIMGV) *** #
    def simgv_open(self):
        self.simgv_open_image()
        self.SimpleImageViewer.show()

    def simgv_open_image(self):
        items_selected = self.ui_main_win.listImage.selectedItems()
        if len(items_selected) > 0:
            self.img_view_index = self.ui_main_win.listImage.row(items_selected[0])
            self.simgv_load_image_to_viewer(self.img_view_index)
        elif len(self.image_list) > 0:
            self.img_view_index = 0
            self.simgv_load_image_to_viewer(self.img_view_index)

    def simgv_load_image_to_viewer(self, index):
        if self.draw_kp:
            img_rgb = self.image_list[index].img_get_img_rgb_with_feature_points()
            feature_point_number = len(self.image_list[index].feature_points.keypoints)
            self.ui_simple_img_viewer.label_feature_points_number.setText(str(feature_point_number))
        else:
            img_rgb = self.image_list[index].img_get_img_rgb()
            self.ui_simple_img_viewer.label_feature_points_number.clear()
        bytes_per_line = 3 * self.image_list[index].info.width
        q_img = QImage(img_rgb, self.image_list[index].info.width, self.image_list[index].info.height,
                                bytes_per_line, QImage.Format_RGB888)
        width = self.ui_simple_img_viewer.image_view.width()
        height = self.ui_simple_img_viewer.image_view.height()
        if q_img.width() < width or q_img.height() < height:
            width = q_img.width()
            height = q_img.height()
        size = QSize(width, height)
        pixmap = QPixmap()
        pixmap = pixmap.fromImage(q_img)
        pixmap = pixmap.scaled(size, self.Q_ASPECT_RATIO)
        self.ui_simple_img_viewer.image_view.setPixmap(pixmap)
        self.ui_simple_img_viewer.image_view.show()

        self.ui_simple_img_viewer.button_previous.setEnabled(self.UP)
        self.ui_simple_img_viewer.button_next.setEnabled(self.UP)
        if index == 0:
            self.ui_simple_img_viewer.button_previous.setEnabled(self.DOWN)
        if index == len(self.image_list) - 1:
            self.ui_simple_img_viewer.button_next.setEnabled(self.DOWN)

    def simgv_button_previous(self):
        self.img_view_index -= 1
        self.simgv_load_image_to_viewer(self.img_view_index)

    def simgv_button_next(self):
        self.img_view_index += 1
        self.simgv_load_image_to_viewer(self.img_view_index)

    def simgv_kp_view_check(self):
        self.draw_kp = self.ui_simple_img_viewer.check_box_draw_keypoints.isChecked()
        self.simgv_load_image_to_viewer(self.img_view_index)

    # *** VIDEOS *** #

    def video_import(self):
        """
        Take the path(s) of one or more videos and import them to the application.
        :return:
        """
        file_dialog = QFileDialog()
        f_path = file_dialog.getOpenFileNames(parent=None,
                                              caption="Open Video(s)",
                                              directory=QDir.homePath(),
                                              filter=self.VID_FILTER,
                                              options=self.DIALOG_FLAG)[0]
        if f_path:
            for file in f_path:
                video_tmp = Video()
                success = video_tmp.vid_open(file)
                if success:
                    self.video_list.append(video_tmp)
                    item_name = "../" + video_tmp.info.dir_name + "/" + video_tmp.info.name
                    item_widget = QListWidgetItem(item_name)
                    item_widget.setFlags(item_widget.flags() | QtCore.Qt.ItemIsUserCheckable)
                    item_widget.setCheckState(QtCore.Qt.Checked)
                    self.ui_main_win.listVideo.addItem(item_widget)
            self.video_list_info()

    def video_delete(self):
        """
        Delete a video from the list
        :return: Nothing
        """
        item_list = self.ui_main_win.listVideo.selectedItems()
        if not item_list:
            return
        for item in item_list:
            self.video_list.pop(self.ui_main_win.listVideo.row(item))
            self.ui_main_win.listVideo.takeItem(self.ui_main_win.listVideo.row(item))
        self.video_list_info()

    def video_list_info(self):
        """
        Print the video list info in a console window (for debugging)
        :return: Nothing
        """
        for video in self.video_list:
            video.vid_print_info()

    # *** VIDEO 2 IMAGES *** #

    def video2images(self):
        """
        Open the video2images dialog.
        :return: Nothing
        """
        self.video2images_set_default()
        self.Video2Images.show()

    def video2images_set_default(self):
        """
        Set the default parameters for video2images dialog
        :return: Nothing
        """
        item_list_size = self.ui_main_win.listVideo.count()
        for item_id in range(0, item_list_size):
            if self.ui_main_win.listVideo.item(item_id).checkState():
                item_name = self.ui_main_win.listVideo.item(item_id).text()
                self.ui_video2images.combo_box_select_video.addItem(item_name)
                self.ui_video2images.line_edit_export_images_at.setEnabled(self.UP)
                self.ui_video2images.button_export_images_at.setEnabled(self.UP)

        self.ui_video2images.combo_box_select_video.setCurrentIndex(0)
        self.video2images_set_fps_for_video()

    def video2images_set_fps_for_video(self):
        video_name = self.ui_video2images.combo_box_select_video.currentText()
        item_list_size = self.ui_main_win.listVideo.count()
        for item_id in range(0, item_list_size):
            item_name = self.ui_main_win.listVideo.item(item_id).text()
            if video_name == item_name:
                fps = self.video_list[item_id].FPS()
                self.ui_video2images.spin_box_fps.setValue(fps)

    def video2images_set_export_folder(self):
        file_dialog = QFileDialog()
        f_path = file_dialog.getExistingDirectory(parent=None,
                                                  caption="Open Directory",
                                                  directory=QDir.homePath(),
                                                  options=self.DIALOG_FLAG | QFileDialog.ShowDirsOnly)
        # print(f_path)
        if f_path:
            self.ui_video2images.line_edit_export_images_at.setText(f_path)
            self.ui_video2images.button_compute.setEnabled(self.UP)

    def video2images_clear(self):
        self.ui_video2images.combo_box_select_video.clear()
        self.ui_video2images.spin_box_fps.setValue(1)
        self.ui_video2images.line_edit_export_images_at.setEnabled(self.DOWN)
        self.ui_video2images.button_export_images_at.setEnabled(self.DOWN)
        self.ui_video2images.button_compute.setEnabled(self.DOWN)

    def video2images_cancel(self):
        self.video2images_clear()
        self.Video2Images.close()

    def video2images_compute(self):
        video_name = self.ui_video2images.combo_box_select_video.currentText()
        export_folder_name = self.ui_video2images.line_edit_export_images_at.text()
        fps = self.ui_video2images.spin_box_fps.value()
        export_folder_name += "/"
        self.video2images_compute_yes(video_name, export_folder_name, fps)
        message_box_widget = QWidget()
        QMessageBox.information(message_box_widget, "img2video", "Process finished successfully!")

    def video2images_compute_yes(self, video_name, export_folder_name, fps):
        item_list_size = self.ui_main_win.listVideo.count()
        for item_id in range(0, item_list_size):
            item_name = self.ui_main_win.listVideo.item(item_id).text()
            if video_name == item_name:
                self.video_list[item_id].video2img(export_folder_name, fps)
                break
