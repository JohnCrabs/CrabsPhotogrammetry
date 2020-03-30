import sys
from ui_wins.mainwin import *
from ui_wins.video2images import *

from PyQt5.Qt import (Qt, QDir, QFileDialog, QListWidgetItem)

from lib.video import *
from lib.image import *


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
        # ------------------------
        # Flags Section ends here
        # ---------------------------------------------------------------------------------------------------------- #
        #
        # ------------------------
        # Set class items
        # ------------------------
        self.video_list = []
        self.image_list = []
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
        self.Video2Images = QtWidgets.QDialog()
        self.ui_video2images.setupUi(self.Video2Images)

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
        # *** VIDEO *** #
        self.ui_main_win.actionVideoImport.triggered.connect(self.video_import)  # actionVideoImport
        self.ui_main_win.actionVideo_to_Images.triggered.connect(self.video2images) # actionVideo_to_Images
        self.ui_main_win.button_add_video.clicked.connect(self.video_import)  # button_add_video
        self.ui_main_win.button_del_video.clicked.connect(self.video_delete)  # button_del_video

        # *** UI_VIDEO_2_IMAGES *** #
        self.ui_video2images.button_cancel.clicked.connect(self.video2images_cancel)

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
            for file in f_path:
                image_tmp = Image()
                success = image_tmp.img_import(file)
                if success:
                    image_tmp.img_print_info()
                    self.video_list.append(image_tmp)
                    item_name = "../" + image_tmp.info.dir_name + "/" + image_tmp.info.name
                    item_widget = QListWidgetItem(item_name)
                    item_widget.setFlags(item_widget.flags() | QtCore.Qt.ItemIsUserCheckable)
                    item_widget.setCheckState(QtCore.Qt.Checked)
                    self.ui_main_win.listVideo.addItem(item_widget)

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
        self.image_list_info()

    def image_list_info(self):
        for image in self.image_list:
            image.img_print_info()

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
        for video in self.video_list:
            video.vid_print_info()

    def video2images(self):
        self.Video2Images.show()

    def video2images_cancel(self):
        self.Video2Images.close()
