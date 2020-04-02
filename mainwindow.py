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
        self.ui_main_win.actionCreate_Model.triggered.connect(self.image_create_model)

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
        self.MainWindow.show()  # Main Loop
        sys.exit(self.app.exec_())  # Close application
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
        file_dialog = QFileDialog()  # Create QFileDialog
        # Open the file dialog as Open File Names dialog (for image choice)
        f_path = file_dialog.getOpenFileNames(parent=None,
                                              caption="Open Image(s)",
                                              directory=QDir.homePath(),
                                              filter=self.IMG_FILTER,
                                              options=self.DIALOG_FLAG)[0]
        if f_path:  # If user chose at least one image
            img_id_counter = 0  # Set a counter for id
            for file in f_path:  # For all paths in f_paths
                image_tmp = Image()  # Create an Image object
                success = image_tmp.img_open(file)  # Set image parameters
                if success:  # If image exists
                    image_tmp.img_set_image_id(img_id_counter)  # Set image counter
                    img_id_counter += 1  # increase the counter by 1
                    # image_tmp.img_print_info()  # print image info for debugging
                    self.image_list.append(image_tmp)  # Append image to list
                    item_name = "../" + image_tmp.info.dir_name + "/" + image_tmp.info.name  # Set name for view
                    item_widget = QListWidgetItem(item_name)  # Append item to window image list
                    item_widget.setFlags(item_widget.flags() | QtCore.Qt.ItemIsUserCheckable)  # Set it checkable
                    item_widget.setCheckState(QtCore.Qt.Checked)  # Set it checked
                    self.ui_main_win.listImage.addItem(item_widget)  # Add item to list
                    self.ui_main_win.menuCamera_Settings.setEnabled(self.UP)  # Enable Camera menu

    def image_delete(self):
        """
        Delete an image from the list
        :return: Nothing
        """
        item_list = self.ui_main_win.listImage.selectedItems()  # Take all selected indexes
        if not item_list:  # If nothing is selected
            return  # return
        for item in item_list:  # else for each selected item
            self.image_list.pop(self.ui_main_win.listImage.row(item))  # delete the item from python image_list
            self.ui_main_win.listImage.takeItem(self.ui_main_win.listImage.row(item))  # delete it from Qt image list
        image_list_counter = 0  # set image id counter to 0
        for image in self.image_list:  # for each image in image list
            image.img_set_image_id(image_list_counter)  # set new id
            image_list_counter += 1  # increase the counter by 1
        # self.image_list_info()  # show new image info list for debugging

    def image_list_info(self):
        """
        Print to console the information of images in the list.
        :return: Nothing
        """
        for image in self.image_list:  # for each image in image list
            image.img_print_info()  # print image info to the console

    def image_default_approximate_camera_checked(self):
        """
        Reset action Approximate Interior Orientation
        :return: Nothing
        """
        self.ui_main_win.actionApproximate_Interior_Orientation.setChecked(self.DOWN)

    def image_approximate_camera(self):
        """
        Approximate the camera interior orientation for each image in image list.
        :return: Nothing
        """
        success = False  # set success boolean to false
        for image in self.image_list:  # for each image in image list
            success = True  # set success to True (this means there are images in the list)
            image.img_approximate_camera_parameters()  # approximate camera parameters
            # image.img_print_camera_matrix()  # print camera matrix for debugging
        # self.image_list[0].img_print_camera_matrix()  # print the camera matrix only for the first image (debugging)
        if success:  # if success = True
            self.ui_main_win.menuFind_Feature_Points.setEnabled(self.UP)  # enable menu find feature points
            # check action approximate interior orientation
            self.ui_main_win.actionApproximate_Interior_Orientation.setChecked(self.UP)
            message_box_widget = QWidget()  # create QWidget
            QMessageBox.information(message_box_widget, "Approximate Interior Orientation",
                                    "Process finished successfully!")  # information message

    def image_default_find_feature_points_checked(self):
        """
        Reset the actions SIFT, SURF, ORB and AKAZE.
        :return: Nothing
        """
        self.ui_main_win.actionSIFT.setChecked(self.DOWN)
        self.ui_main_win.actionSURF.setChecked(self.DOWN)
        self.ui_main_win.actionORB.setChecked(self.DOWN)
        self.ui_main_win.actionAKAZE.setChecked(self.DOWN)

    def image_find_feature_points(self, flag=IMG_AKAZE):
        """
        Use the appropriate flag and find the feature points for each image in the list.
        It takes a while to calculate for big images.
        :param flag: IMG_SIFT, IMG_SURF, IMG_ORB, IMG_AKAZE
        :return: Nothing
        """
        success = False  # Set success to False
        for image in self.image_list:  # For each image in image list
            success = True  # Set success to True (this means there are images in list)
            image.img_find_feature_points(flag=flag)  # find feature points using the specified flag
        if success:  # if success = True
            self.image_default_find_feature_points_checked()  # reset the find feature checked
            # reset the default create block (do this because this function doesnt recreate the block). The block needs
            # to be recreated after find feature points action for updated results.
            self.image_default_create_block_checked()
            if flag == self.F_AKAZE:  # if flag AKAZE
                self.ui_main_win.actionAKAZE.setChecked(self.UP)  # find feature points using akaze method
            elif flag == self.F_ORB:  # if flag ORB
                self.ui_main_win.actionORB.setChecked(self.UP)  # find feature points using orb method
            self.ui_simple_img_viewer.check_box_draw_keypoints.setEnabled(self.UP)  # enable draw keypoints to simgv
            self.ui_simple_img_viewer.check_box_draw_keypoints.setChecked(self.DOWN)  # uncheck it
            self.draw_kp = self.DOWN  # set the draw kp boolean to uncheck (use this for code readability)
            self.ui_main_win.actionCreate_Block.setEnabled(self.UP)  # enable action Create Block
            message_box_widget = QWidget()  # Create QWidget
            QMessageBox.information(message_box_widget, flag,
                                    "Process finished successfully!")  # message information

    def image_default_create_block_checked(self):
        """
        Reset the action Create Block.
        :return: Nothing
        """
        self.ui_main_win.actionCreate_Block.setChecked(self.DOWN)

    def image_create_block(self):
        """
        Create a block of images for all checked images in image list.
        :return: Nothing
        """
        image_list_tmp = []  # create a temporary image list
        image_list_size = len(self.image_list)  # take the size of the actual list
        success = False  # set success boolean to False
        counter = 0  # set image in image_list_tmp counter to 0
        for index_id in range(0, image_list_size):  # for index id in range(0, list_size)
            if self.ui_main_win.listImage.item(index_id).checkState():  # check the image item state (if true)
                counter += 1  # increase the counter
                if counter > 1:  # a block needs at least 2 images (if counter > 1)
                    success = True  # set success to True
                image_list_tmp.append(self.image_list[index_id])  # append the image from image list to tmp image list
        # print(image_list_tmp)  # print image list for debugging
        if success:  # if success = True
            self.ui_main_win.actionCreate_Block.setChecked(self.UP)  # check Create Block
            self.image_block.b_img_create_image_list(image_list_tmp)  # set the image block
            self.ui_main_win.menuImage_Matching.setEnabled(self.UP)  # enable menu Image Matching
            message_box_widget = QWidget()  # create QWidget
            QMessageBox.information(message_box_widget, "Create Block",
                                    "Process finished successfully!")  # message information

    def image_default_matching(self):
        """
        Reset actions All Images Matching and Fast Matching
        :return: Nothing
        """
        self.ui_main_win.actionAll_Images_Matching.setChecked(self.DOWN)
        self.ui_main_win.actionFast_Matching.setChecked(self.DOWN)

    def image_matching(self, fast=False):
        """
        If fast=True run fast matching method. Else run block matching method (match all images).
        :param fast: True/False
        :return: Nothing
        """
        if fast:
            self.image_default_matching()
            self.image_block.b_img_fast_matching()
            message_box_widget = QWidget()  # create QWidget
            self.ui_main_win.actionFast_Matching.setChecked(self.UP)
            QMessageBox.information(message_box_widget, "Fast Matching",
                                    "Process finished successfully!")  # message information
            self.ui_main_win.actionCreate_Model.setEnabled(self.UP)
        else:
            self.image_default_matching()
            self.image_block.b_img_match_all_images()
            self.ui_main_win.actionAll_Images_Matching.setChecked(self.UP)
            message_box_widget = QWidget()  # create QWidget
            QMessageBox.information(message_box_widget, "Matching All Images",
                                    "Process finished successfully!")  # message information
            self.ui_main_win.actionCreate_Model.setEnabled(self.UP)

    def image_create_model(self):
        self.image_block.b_img_create_pair_models()

    # *** SIMPLE IMAGE VIEWER (SIMGV) *** #
    def simgv_open(self):
        """
        Open image and then Simple Image Viewer window.
        :return: Nothing
        """
        self.simgv_open_image()
        self.SimpleImageViewer.show()

    def simgv_open_image(self):
        """
        Open the first selected image. If none of the images is selected, then open the first image.
        If the list has no image, then open the default image viewer.
        :return: Nothing
        """
        items_selected = self.ui_main_win.listImage.selectedItems()  # take all selected items
        if len(items_selected) > 0:  # if there is at least one item selected
            self.img_view_index = self.ui_main_win.listImage.row(items_selected[0])  # take the first selected item
            self.simgv_load_image_to_viewer(self.img_view_index)  # load it to viewer
        elif len(self.image_list) > 0:  # else if there are no selected items, but there are images imported
            self.img_view_index = 0  # set the view index to the first image in the least
            self.simgv_load_image_to_viewer(self.img_view_index)  # load the first image to the viewer

    def simgv_load_image_to_viewer(self, index):
        """
        Load an image to viewer. If the show feature points is checked, then load feature points as well.
        This option can be done only if the user has run a feature point method first.
        :param index: index of image to load.
        :return: Nothing
        """
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
        """
        Set the image index to -1 (if index is greater than 0) and load that image to viewer.
        :return: Nothing
        """
        self.img_view_index -= 1  # decrease the image view index by 1
        self.simgv_load_image_to_viewer(self.img_view_index)  # load that image to viewer

    def simgv_button_next(self):
        """
        Set the image index to +1 (if index is greater than 0) and load that image to viewer.
        :return: Nothing
        """
        self.img_view_index += 1  # increase the image view index by 1
        self.simgv_load_image_to_viewer(self.img_view_index)  # load that image to viewer

    def simgv_kp_view_check(self):
        """
        Check if feature points checkbox is checked and load the correct image
        :return: Nothing
        """
        self.draw_kp = self.ui_simple_img_viewer.check_box_draw_keypoints.isChecked()  # take the checked boolean value
        self.simgv_load_image_to_viewer(self.img_view_index)  # load the image to viewer

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
        """
        Set the fps from video 2 images spin box.
        :return: Nothing
        """
        video_name = self.ui_video2images.combo_box_select_video.currentText()
        item_list_size = self.ui_main_win.listVideo.count()
        for item_id in range(0, item_list_size):
            item_name = self.ui_main_win.listVideo.item(item_id).text()
            if video_name == item_name:
                fps = self.video_list[item_id].FPS()
                self.ui_video2images.spin_box_fps.setValue(fps)

    def video2images_set_export_folder(self):
        """
        Set export folder for the video frames.
        :return: Nothing
        """
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
        """
        Clear video 2 images window (reset the window)
        :return: Nothing
        """
        self.ui_video2images.combo_box_select_video.clear()
        self.ui_video2images.spin_box_fps.setValue(1)
        self.ui_video2images.line_edit_export_images_at.setEnabled(self.DOWN)
        self.ui_video2images.button_export_images_at.setEnabled(self.DOWN)
        self.ui_video2images.button_compute.setEnabled(self.DOWN)

    def video2images_cancel(self):
        """
        Clear the video 2 images window and close the window.
        :return: Nothing
        """
        self.video2images_clear()
        self.Video2Images.close()

    def video2images_compute(self):
        """
        Executed when the user press compute and export the video frames to the given folder.
        :return: Nothing
        """
        video_name = self.ui_video2images.combo_box_select_video.currentText()
        export_folder_name = self.ui_video2images.line_edit_export_images_at.text()
        fps = self.ui_video2images.spin_box_fps.value()
        export_folder_name += "/"
        self.video2images_compute_yes(video_name, export_folder_name, fps)
        message_box_widget = QWidget()
        QMessageBox.information(message_box_widget, "img2video", "Process finished successfully!")

    def video2images_compute_yes(self, video_name, export_folder_name, fps):
        """
        Export the frames to the given folder.
        :param video_name: the name of the video
        :param export_folder_name: the path to the exported folder
        :param fps: the number of fps (use it to find the frames to export)
        :return: Nothing
        """
        item_list_size = self.ui_main_win.listVideo.count()
        for item_id in range(0, item_list_size):
            item_name = self.ui_main_win.listVideo.item(item_id).text()
            if video_name == item_name:
                self.video_list[item_id].video2img(export_folder_name, fps)
                break
