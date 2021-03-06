# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwin.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(520, 520)
        MainWindow.setMinimumSize(QtCore.QSize(520, 520))
        MainWindow.setMaximumSize(QtCore.QSize(520, 520))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_Image = QtWidgets.QWidget()
        self.tab_Image.setObjectName("tab_Image")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab_Image)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.image_button_widget = QtWidgets.QWidget(self.tab_Image)
        self.image_button_widget.setMinimumSize(QtCore.QSize(200, 30))
        self.image_button_widget.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.image_button_widget.setObjectName("image_button_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.image_button_widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_image_list = QtWidgets.QLabel(self.image_button_widget)
        self.label_image_list.setMinimumSize(QtCore.QSize(0, 15))
        self.label_image_list.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_image_list.setFont(font)
        self.label_image_list.setObjectName("label_image_list")
        self.verticalLayout_2.addWidget(self.label_image_list)
        self.listImage = QtWidgets.QListWidget(self.image_button_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listImage.sizePolicy().hasHeightForWidth())
        self.listImage.setSizePolicy(sizePolicy)
        self.listImage.setMinimumSize(QtCore.QSize(185, 0))
        self.listImage.setMaximumSize(QtCore.QSize(900, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.listImage.setFont(font)
        self.listImage.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.listImage.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.listImage.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listImage.setObjectName("listImage")
        self.verticalLayout_2.addWidget(self.listImage)
        self.button_add_image = QtWidgets.QPushButton(self.image_button_widget)
        self.button_add_image.setMinimumSize(QtCore.QSize(0, 25))
        self.button_add_image.setObjectName("button_add_image")
        self.verticalLayout_2.addWidget(self.button_add_image)
        self.button_del_image = QtWidgets.QPushButton(self.image_button_widget)
        self.button_del_image.setMinimumSize(QtCore.QSize(0, 25))
        self.button_del_image.setObjectName("button_del_image")
        self.verticalLayout_2.addWidget(self.button_del_image)
        self.horizontalLayout.addWidget(self.image_button_widget)
        self.tabWidget.addTab(self.tab_Image, "")
        self.tab_Video = QtWidgets.QWidget()
        self.tab_Video.setObjectName("tab_Video")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab_Video)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.video_button_widget = QtWidgets.QWidget(self.tab_Video)
        self.video_button_widget.setMinimumSize(QtCore.QSize(200, 30))
        self.video_button_widget.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.video_button_widget.setObjectName("video_button_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.video_button_widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_video_list = QtWidgets.QLabel(self.video_button_widget)
        self.label_video_list.setMinimumSize(QtCore.QSize(0, 15))
        self.label_video_list.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_video_list.setFont(font)
        self.label_video_list.setObjectName("label_video_list")
        self.verticalLayout.addWidget(self.label_video_list)
        self.listVideo = QtWidgets.QListWidget(self.video_button_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listVideo.sizePolicy().hasHeightForWidth())
        self.listVideo.setSizePolicy(sizePolicy)
        self.listVideo.setMinimumSize(QtCore.QSize(185, 0))
        self.listVideo.setMaximumSize(QtCore.QSize(900, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.listVideo.setFont(font)
        self.listVideo.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.listVideo.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.listVideo.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.listVideo.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listVideo.setObjectName("listVideo")
        self.verticalLayout.addWidget(self.listVideo)
        self.button_add_video = QtWidgets.QPushButton(self.video_button_widget)
        self.button_add_video.setMinimumSize(QtCore.QSize(0, 25))
        self.button_add_video.setObjectName("button_add_video")
        self.verticalLayout.addWidget(self.button_add_video)
        self.button_del_video = QtWidgets.QPushButton(self.video_button_widget)
        self.button_del_video.setMinimumSize(QtCore.QSize(0, 25))
        self.button_del_video.setObjectName("button_del_video")
        self.verticalLayout.addWidget(self.button_del_video)
        self.horizontalLayout_3.addWidget(self.video_button_widget)
        self.tabWidget.addTab(self.tab_Video, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 520, 18))
        self.menubar.setObjectName("menubar")
        self.menuImage = QtWidgets.QMenu(self.menubar)
        self.menuImage.setObjectName("menuImage")
        self.menuProcessing = QtWidgets.QMenu(self.menuImage)
        self.menuProcessing.setObjectName("menuProcessing")
        self.menuFind_Feature_Points = QtWidgets.QMenu(self.menuProcessing)
        self.menuFind_Feature_Points.setEnabled(False)
        self.menuFind_Feature_Points.setObjectName("menuFind_Feature_Points")
        self.menuImage_Matching = QtWidgets.QMenu(self.menuProcessing)
        self.menuImage_Matching.setEnabled(False)
        self.menuImage_Matching.setObjectName("menuImage_Matching")
        self.menuCamera_Settings = QtWidgets.QMenu(self.menuProcessing)
        self.menuCamera_Settings.setEnabled(False)
        self.menuCamera_Settings.setObjectName("menuCamera_Settings")
        self.menuVideo = QtWidgets.QMenu(self.menubar)
        self.menuVideo.setObjectName("menuVideo")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionVideoImport = QtWidgets.QAction(MainWindow)
        self.actionVideoImport.setObjectName("actionVideoImport")
        self.actionVideoExport = QtWidgets.QAction(MainWindow)
        self.actionVideoExport.setObjectName("actionVideoExport")
        self.actionVideo_to_Images = QtWidgets.QAction(MainWindow)
        self.actionVideo_to_Images.setObjectName("actionVideo_to_Images")
        self.actionImageImport = QtWidgets.QAction(MainWindow)
        self.actionImageImport.setObjectName("actionImageImport")
        self.actionImageExport = QtWidgets.QAction(MainWindow)
        self.actionImageExport.setObjectName("actionImageExport")
        self.actionImage_Viewer = QtWidgets.QAction(MainWindow)
        self.actionImage_Viewer.setObjectName("actionImage_Viewer")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionSIFT = QtWidgets.QAction(MainWindow)
        self.actionSIFT.setCheckable(True)
        self.actionSIFT.setEnabled(False)
        self.actionSIFT.setObjectName("actionSIFT")
        self.actionSURF = QtWidgets.QAction(MainWindow)
        self.actionSURF.setCheckable(True)
        self.actionSURF.setEnabled(False)
        self.actionSURF.setObjectName("actionSURF")
        self.actionORB = QtWidgets.QAction(MainWindow)
        self.actionORB.setCheckable(True)
        self.actionORB.setObjectName("actionORB")
        self.actionAKAZE = QtWidgets.QAction(MainWindow)
        self.actionAKAZE.setCheckable(True)
        self.actionAKAZE.setObjectName("actionAKAZE")
        self.actionAll_Images_Matching = QtWidgets.QAction(MainWindow)
        self.actionAll_Images_Matching.setCheckable(True)
        self.actionAll_Images_Matching.setObjectName("actionAll_Images_Matching")
        self.actionFast_Matching = QtWidgets.QAction(MainWindow)
        self.actionFast_Matching.setCheckable(True)
        self.actionFast_Matching.setObjectName("actionFast_Matching")
        self.actionApproximate_Interior_Orientation = QtWidgets.QAction(MainWindow)
        self.actionApproximate_Interior_Orientation.setCheckable(True)
        self.actionApproximate_Interior_Orientation.setObjectName("actionApproximate_Interior_Orientation")
        self.actionCreate_Block = QtWidgets.QAction(MainWindow)
        self.actionCreate_Block.setCheckable(True)
        self.actionCreate_Block.setEnabled(False)
        self.actionCreate_Block.setObjectName("actionCreate_Block")
        self.actionCreate_Model = QtWidgets.QAction(MainWindow)
        self.actionCreate_Model.setCheckable(False)
        self.actionCreate_Model.setEnabled(False)
        self.actionCreate_Model.setObjectName("actionCreate_Model")
        self.actionCrabSFM = QtWidgets.QAction(MainWindow)
        self.actionCrabSFM.setEnabled(False)
        self.actionCrabSFM.setObjectName("actionCrabSFM")
        self.menuFind_Feature_Points.addAction(self.actionSIFT)
        self.menuFind_Feature_Points.addAction(self.actionSURF)
        self.menuFind_Feature_Points.addAction(self.actionORB)
        self.menuFind_Feature_Points.addAction(self.actionAKAZE)
        self.menuImage_Matching.addAction(self.actionAll_Images_Matching)
        self.menuImage_Matching.addAction(self.actionFast_Matching)
        self.menuCamera_Settings.addAction(self.actionApproximate_Interior_Orientation)
        self.menuProcessing.addAction(self.menuCamera_Settings.menuAction())
        self.menuProcessing.addAction(self.menuFind_Feature_Points.menuAction())
        self.menuProcessing.addAction(self.actionCreate_Block)
        self.menuProcessing.addAction(self.menuImage_Matching.menuAction())
        self.menuProcessing.addAction(self.actionCreate_Model)
        self.menuProcessing.addSeparator()
        self.menuProcessing.addAction(self.actionCrabSFM)
        self.menuImage.addAction(self.actionImageImport)
        self.menuImage.addAction(self.actionImageExport)
        self.menuImage.addSeparator()
        self.menuImage.addAction(self.actionImage_Viewer)
        self.menuImage.addSeparator()
        self.menuImage.addAction(self.menuProcessing.menuAction())
        self.menuVideo.addAction(self.actionVideoImport)
        self.menuVideo.addAction(self.actionVideoExport)
        self.menuVideo.addSeparator()
        self.menuVideo.addAction(self.actionVideo_to_Images)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuImage.menuAction())
        self.menubar.addAction(self.menuVideo.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Crabs Photogrammetry"))
        self.label_image_list.setText(_translate("MainWindow", "Image List:"))
        self.button_add_image.setText(_translate("MainWindow", "Add Image"))
        self.button_del_image.setText(_translate("MainWindow", "Delete Selected"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Image), _translate("MainWindow", "Image"))
        self.label_video_list.setText(_translate("MainWindow", "Video List:"))
        self.button_add_video.setText(_translate("MainWindow", "Add Video"))
        self.button_del_video.setText(_translate("MainWindow", "Delete Selected"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Video), _translate("MainWindow", "Video"))
        self.menuImage.setTitle(_translate("MainWindow", "Image"))
        self.menuProcessing.setTitle(_translate("MainWindow", "Processing"))
        self.menuFind_Feature_Points.setTitle(_translate("MainWindow", "Find Feature Points"))
        self.menuImage_Matching.setTitle(_translate("MainWindow", "Image Matching"))
        self.menuCamera_Settings.setTitle(_translate("MainWindow", "Camera Settings"))
        self.menuVideo.setTitle(_translate("MainWindow", "Video"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionVideoImport.setText(_translate("MainWindow", "Import"))
        self.actionVideoExport.setText(_translate("MainWindow", "Export"))
        self.actionVideo_to_Images.setText(_translate("MainWindow", "Video to Images"))
        self.actionImageImport.setText(_translate("MainWindow", "Import"))
        self.actionImageExport.setText(_translate("MainWindow", "Export"))
        self.actionImage_Viewer.setText(_translate("MainWindow", "Image Viewer"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionSIFT.setText(_translate("MainWindow", "SIFT"))
        self.actionSURF.setText(_translate("MainWindow", "SURF"))
        self.actionORB.setText(_translate("MainWindow", "ORB"))
        self.actionAKAZE.setText(_translate("MainWindow", "AKAZE"))
        self.actionAll_Images_Matching.setText(_translate("MainWindow", "All Images"))
        self.actionFast_Matching.setText(_translate("MainWindow", "Fast Matching"))
        self.actionApproximate_Interior_Orientation.setText(_translate("MainWindow", "Approximate Interior Orientation"))
        self.actionCreate_Block.setText(_translate("MainWindow", "Create Block"))
        self.actionCreate_Model.setText(_translate("MainWindow", "Create Model"))
        self.actionCrabSFM.setText(_translate("MainWindow", "CrabSFM"))
