# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simple_image_viewer.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SimpleImageViewer(object):
    def setupUi(self, SimpleImageViewer):
        SimpleImageViewer.setObjectName("SimpleImageViewer")
        SimpleImageViewer.resize(1100, 720)
        SimpleImageViewer.setMinimumSize(QtCore.QSize(1100, 720))
        SimpleImageViewer.setMaximumSize(QtCore.QSize(1100, 720))
        self.verticalLayout = QtWidgets.QVBoxLayout(SimpleImageViewer)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_image_view = QtWidgets.QWidget(SimpleImageViewer)
        self.widget_image_view.setMinimumSize(QtCore.QSize(0, 600))
        self.widget_image_view.setMaximumSize(QtCore.QSize(16777215, 650))
        self.widget_image_view.setObjectName("widget_image_view")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_image_view)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.image_view = QtWidgets.QLabel(self.widget_image_view)
        self.image_view.setMinimumSize(QtCore.QSize(1024, 512))
        self.image_view.setMaximumSize(QtCore.QSize(1024, 640))
        self.image_view.setFrameShape(QtWidgets.QFrame.Box)
        self.image_view.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.image_view.setText("")
        self.image_view.setAlignment(QtCore.Qt.AlignCenter)
        self.image_view.setObjectName("image_view")
        self.horizontalLayout_3.addWidget(self.image_view)
        self.verticalLayout.addWidget(self.widget_image_view)
        self.widget_for_buttons = QtWidgets.QWidget(SimpleImageViewer)
        self.widget_for_buttons.setObjectName("widget_for_buttons")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_for_buttons)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_next_previous = QtWidgets.QWidget(self.widget_for_buttons)
        self.widget_next_previous.setObjectName("widget_next_previous")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_next_previous)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_previous = QtWidgets.QPushButton(self.widget_next_previous)
        self.button_previous.setEnabled(False)
        self.button_previous.setObjectName("button_previous")
        self.horizontalLayout_2.addWidget(self.button_previous)
        self.button_next = QtWidgets.QPushButton(self.widget_next_previous)
        self.button_next.setEnabled(False)
        self.button_next.setObjectName("button_next")
        self.horizontalLayout_2.addWidget(self.button_next)
        self.horizontalLayout.addWidget(self.widget_next_previous)
        self.widget_basic_image_processing = QtWidgets.QWidget(self.widget_for_buttons)
        self.widget_basic_image_processing.setObjectName("widget_basic_image_processing")
        self.horizontalLayout.addWidget(self.widget_basic_image_processing)
        self.verticalLayout.addWidget(self.widget_for_buttons)

        self.retranslateUi(SimpleImageViewer)
        QtCore.QMetaObject.connectSlotsByName(SimpleImageViewer)

    def retranslateUi(self, SimpleImageViewer):
        _translate = QtCore.QCoreApplication.translate
        SimpleImageViewer.setWindowTitle(_translate("SimpleImageViewer", "Simple Image Viewer"))
        self.button_previous.setText(_translate("SimpleImageViewer", "Previous"))
        self.button_previous.setShortcut(_translate("SimpleImageViewer", "Left"))
        self.button_next.setText(_translate("SimpleImageViewer", "Next"))
        self.button_next.setShortcut(_translate("SimpleImageViewer", "Right"))

