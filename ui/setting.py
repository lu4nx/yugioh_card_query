# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_settings(object):
    def setupUi(self, settings):
        settings.setObjectName("settings")
        settings.resize(409, 153)
        self.card_pictures_label = QtWidgets.QLabel(settings)
        self.card_pictures_label.setGeometry(QtCore.QRect(20, 10, 55, 18))
        self.card_pictures_label.setObjectName("card_pictures_label")
        self.card_pictures_path_edit = QtWidgets.QLineEdit(settings)
        self.card_pictures_path_edit.setGeometry(QtCore.QRect(80, 10, 231, 30))
        self.card_pictures_path_edit.setObjectName("card_pictures_path_edit")
        self.card_database_label = QtWidgets.QLabel(settings)
        self.card_database_label.setGeometry(QtCore.QRect(20, 60, 61, 18))
        self.card_database_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.card_database_label.setObjectName("card_database_label")
        self.card_database_path_edit = QtWidgets.QLineEdit(settings)
        self.card_database_path_edit.setGeometry(QtCore.QRect(80, 60, 231, 30))
        self.card_database_path_edit.setObjectName("card_database_path_edit")
        self.save_setting_button = QtWidgets.QPushButton(settings)
        self.save_setting_button.setGeometry(QtCore.QRect(20, 110, 85, 27))
        self.save_setting_button.setObjectName("save_setting_button")
        self.select_pic_dir_button = QtWidgets.QPushButton(settings)
        self.select_pic_dir_button.setGeometry(QtCore.QRect(320, 10, 61, 27))
        self.select_pic_dir_button.setObjectName("select_pic_dir_button")
        self.select_database_file_button = QtWidgets.QPushButton(settings)
        self.select_database_file_button.setGeometry(QtCore.QRect(320, 60, 61, 27))
        self.select_database_file_button.setObjectName("select_database_file_button")

        self.retranslateUi(settings)
        QtCore.QMetaObject.connectSlotsByName(settings)

    def retranslateUi(self, settings):
        _translate = QtCore.QCoreApplication.translate
        settings.setWindowTitle(_translate("settings", "系统设置"))
        self.card_pictures_label.setText(_translate("settings", "卡图路径："))
        self.card_database_label.setText(_translate("settings", "卡库路径："))
        self.save_setting_button.setText(_translate("settings", "保存"))
        self.select_pic_dir_button.setText(_translate("settings", "选择路径"))
        self.select_database_file_button.setText(_translate("settings", "选择文件"))
