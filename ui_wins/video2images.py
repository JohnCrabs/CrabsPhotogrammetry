# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'video2images.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Video2Images(object):
    def setupUi(self, Video2Images):
        Video2Images.setObjectName("Video2Images")
        Video2Images.resize(400, 400)
        Video2Images.setMinimumSize(QtCore.QSize(400, 400))
        Video2Images.setMaximumSize(QtCore.QSize(400, 400))
        self.verticalLayout = QtWidgets.QVBoxLayout(Video2Images)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_option = QtWidgets.QWidget(Video2Images)
        self.widget_option.setObjectName("widget_option")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_option)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_select_video = QtWidgets.QWidget(self.widget_option)
        self.widget_select_video.setObjectName("widget_select_video")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_select_video)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_select_video = QtWidgets.QLabel(self.widget_select_video)
        self.label_select_video.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_select_video.setObjectName("label_select_video")
        self.horizontalLayout_2.addWidget(self.label_select_video)
        self.combo_box_select_video = QtWidgets.QComboBox(self.widget_select_video)
        self.combo_box_select_video.setObjectName("combo_box_select_video")
        self.horizontalLayout_2.addWidget(self.combo_box_select_video)
        self.verticalLayout_2.addWidget(self.widget_select_video)
        self.widget_set_output_folder = QtWidgets.QWidget(self.widget_option)
        self.widget_set_output_folder.setEnabled(True)
        self.widget_set_output_folder.setObjectName("widget_set_output_folder")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_set_output_folder)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_export_images_at = QtWidgets.QLabel(self.widget_set_output_folder)
        self.label_export_images_at.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_export_images_at.setObjectName("label_export_images_at")
        self.verticalLayout_3.addWidget(self.label_export_images_at)
        self.widget_export_images_at = QtWidgets.QWidget(self.widget_set_output_folder)
        self.widget_export_images_at.setObjectName("widget_export_images_at")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_export_images_at)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.line_edit_export_images_at = QtWidgets.QLineEdit(self.widget_export_images_at)
        self.line_edit_export_images_at.setEnabled(False)
        self.line_edit_export_images_at.setAcceptDrops(True)
        self.line_edit_export_images_at.setInputMask("")
        self.line_edit_export_images_at.setReadOnly(True)
        self.line_edit_export_images_at.setObjectName("line_edit_export_images_at")
        self.horizontalLayout_3.addWidget(self.line_edit_export_images_at)
        self.button_export_images_at = QtWidgets.QPushButton(self.widget_export_images_at)
        self.button_export_images_at.setEnabled(False)
        self.button_export_images_at.setMaximumSize(QtCore.QSize(40, 16777215))
        self.button_export_images_at.setObjectName("button_export_images_at")
        self.horizontalLayout_3.addWidget(self.button_export_images_at)
        self.verticalLayout_3.addWidget(self.widget_export_images_at)
        self.verticalLayout_2.addWidget(self.widget_set_output_folder)
        self.widget_set_info = QtWidgets.QWidget(self.widget_option)
        self.widget_set_info.setObjectName("widget_set_info")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_set_info)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.widget_fps = QtWidgets.QWidget(self.widget_set_info)
        self.widget_fps.setObjectName("widget_fps")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_fps)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_fps = QtWidgets.QLabel(self.widget_fps)
        self.label_fps.setObjectName("label_fps")
        self.horizontalLayout_4.addWidget(self.label_fps)
        self.spin_box_fps = QtWidgets.QSpinBox(self.widget_fps)
        self.spin_box_fps.setAlignment(QtCore.Qt.AlignCenter)
        self.spin_box_fps.setMinimum(1)
        self.spin_box_fps.setMaximum(9999)
        self.spin_box_fps.setSingleStep(5)
        self.spin_box_fps.setObjectName("spin_box_fps")
        self.horizontalLayout_4.addWidget(self.spin_box_fps)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.horizontalLayout_5.addWidget(self.widget_fps)
        self.verticalLayout_2.addWidget(self.widget_set_info)
        self.verticalLayout.addWidget(self.widget_option)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.widget_button = QtWidgets.QWidget(Video2Images)
        self.widget_button.setMinimumSize(QtCore.QSize(0, 50))
        self.widget_button.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget_button.setObjectName("widget_button")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_button)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.button_cancel = QtWidgets.QPushButton(self.widget_button)
        self.button_cancel.setObjectName("button_cancel")
        self.horizontalLayout.addWidget(self.button_cancel)
        self.button_compute = QtWidgets.QPushButton(self.widget_button)
        self.button_compute.setEnabled(False)
        self.button_compute.setObjectName("button_compute")
        self.horizontalLayout.addWidget(self.button_compute)
        self.verticalLayout.addWidget(self.widget_button)

        self.retranslateUi(Video2Images)
        QtCore.QMetaObject.connectSlotsByName(Video2Images)

    def retranslateUi(self, Video2Images):
        _translate = QtCore.QCoreApplication.translate
        Video2Images.setWindowTitle(_translate("Video2Images", "Video2Images"))
        self.label_select_video.setText(_translate("Video2Images", "Select Video:"))
        self.label_export_images_at.setText(_translate("Video2Images", "Export Images at:"))
        self.button_export_images_at.setText(_translate("Video2Images", "..."))
        self.label_fps.setText(_translate("Video2Images", "fps:"))
        self.button_cancel.setText(_translate("Video2Images", "Cancel"))
        self.button_compute.setText(_translate("Video2Images", "Compute"))
