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
        settings.resize(401, 202)
        self.gridLayout_2 = QtWidgets.QGridLayout(settings)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.card_pictures_label = QtWidgets.QLabel(settings)
        self.card_pictures_label.setObjectName("card_pictures_label")
        self.gridLayout.addWidget(self.card_pictures_label, 0, 0, 1, 1)
        self.card_pictures_path_edit = QtWidgets.QLineEdit(settings)
        self.card_pictures_path_edit.setObjectName("card_pictures_path_edit")
        self.gridLayout.addWidget(self.card_pictures_path_edit, 0, 1, 1, 1)
        self.select_pic_dir_button = QtWidgets.QPushButton(settings)
        self.select_pic_dir_button.setObjectName("select_pic_dir_button")
        self.gridLayout.addWidget(self.select_pic_dir_button, 0, 2, 1, 1)
        self.card_database_label = QtWidgets.QLabel(settings)
        self.card_database_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.card_database_label.setObjectName("card_database_label")
        self.gridLayout.addWidget(self.card_database_label, 1, 0, 1, 1)
        self.card_database_path_edit = QtWidgets.QLineEdit(settings)
        self.card_database_path_edit.setObjectName("card_database_path_edit")
        self.gridLayout.addWidget(self.card_database_path_edit, 1, 1, 1, 1)
        self.select_database_file_button = QtWidgets.QPushButton(settings)
        self.select_database_file_button.setObjectName("select_database_file_button")
        self.gridLayout.addWidget(self.select_database_file_button, 1, 2, 1, 1)
        self.limit_card_file_label = QtWidgets.QLabel(settings)
        self.limit_card_file_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.limit_card_file_label.setObjectName("limit_card_file_label")
        self.gridLayout.addWidget(self.limit_card_file_label, 2, 0, 1, 1)
        self.limit_card_file_path_edit = QtWidgets.QLineEdit(settings)
        self.limit_card_file_path_edit.setObjectName("limit_card_file_path_edit")
        self.gridLayout.addWidget(self.limit_card_file_path_edit, 2, 1, 1, 1)
        self.select_limit_card_file_button = QtWidgets.QPushButton(settings)
        self.select_limit_card_file_button.setObjectName("select_limit_card_file_button")
        self.gridLayout.addWidget(self.select_limit_card_file_button, 2, 2, 1, 1)
        self.save_setting_button = QtWidgets.QPushButton(settings)
        self.save_setting_button.setObjectName("save_setting_button")
        self.gridLayout.addWidget(self.save_setting_button, 3, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(settings)
        QtCore.QMetaObject.connectSlotsByName(settings)

    def retranslateUi(self, settings):
        _translate = QtCore.QCoreApplication.translate
        settings.setWindowTitle(_translate("settings", "系统设置"))
        self.card_pictures_label.setText(_translate("settings", "卡图路径："))
        self.select_pic_dir_button.setText(_translate("settings", "选择路径"))
        self.card_database_label.setText(_translate("settings", "卡库路径："))
        self.select_database_file_button.setText(_translate("settings", "选择文件"))
        self.limit_card_file_label.setText(_translate("settings", "禁卡数据："))
        self.select_limit_card_file_button.setText(_translate("settings", "选择文件"))
        self.save_setting_button.setText(_translate("settings", "保存"))
