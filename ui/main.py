# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.search_keyword_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.search_keyword_edit.setGeometry(QtCore.QRect(130, 10, 271, 30))
        self.search_keyword_edit.setObjectName("search_keyword_edit")
        self.card_picture = QtWidgets.QLabel(self.centralwidget)
        self.card_picture.setGeometry(QtCore.QRect(300, 50, 221, 301))
        self.card_picture.setObjectName("card_picture")
        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_button.setGeometry(QtCore.QRect(410, 10, 85, 27))
        self.search_button.setObjectName("search_button")
        self.search_type = QtWidgets.QComboBox(self.centralwidget)
        self.search_type.setGeometry(QtCore.QRect(10, 10, 71, 28))
        self.search_type.setObjectName("search_type")
        self.search_type.addItem("")
        self.search_type.addItem("")
        self.search_type.addItem("")
        self.card_info = QtWidgets.QTextBrowser(self.centralwidget)
        self.card_info.setGeometry(QtCore.QRect(280, 360, 256, 192))
        self.card_info.setObjectName("card_info")
        self.search_result_widget = QtWidgets.QListWidget(self.centralwidget)
        self.search_result_widget.setGeometry(QtCore.QRect(10, 50, 256, 501))
        self.search_result_widget.setObjectName("search_result_widget")
        self.history_button = QtWidgets.QPushButton(self.centralwidget)
        self.history_button.setGeometry(QtCore.QRect(90, 10, 31, 27))
        self.history_button.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.history_button.setObjectName("history_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 550, 26))
        self.menubar.setObjectName("menubar")
        self.tools_menu = QtWidgets.QMenu(self.menubar)
        self.tools_menu.setObjectName("tools_menu")
        self.help_menu = QtWidgets.QMenu(self.menubar)
        self.help_menu.setObjectName("help_menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.setting_action = QtWidgets.QAction(MainWindow)
        self.setting_action.setObjectName("setting_action")
        self.about_action = QtWidgets.QAction(MainWindow)
        self.about_action.setObjectName("about_action")
        self.official_website_action = QtWidgets.QAction(MainWindow)
        self.official_website_action.setObjectName("official_website_action")
        self.tools_menu.addAction(self.setting_action)
        self.help_menu.addAction(self.about_action)
        self.help_menu.addAction(self.official_website_action)
        self.menubar.addAction(self.tools_menu.menuAction())
        self.menubar.addAction(self.help_menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "游戏王离线查卡器"))
        self.card_picture.setText(_translate("MainWindow", "TextLabel"))
        self.search_button.setText(_translate("MainWindow", "搜索"))
        self.search_type.setItemText(0, _translate("MainWindow", "卡名"))
        self.search_type.setItemText(1, _translate("MainWindow", "卡码"))
        self.search_type.setItemText(2, _translate("MainWindow", "描述"))
        self.history_button.setText(_translate("MainWindow", "⇦"))
        self.tools_menu.setTitle(_translate("MainWindow", "工具"))
        self.help_menu.setTitle(_translate("MainWindow", "帮助"))
        self.setting_action.setText(_translate("MainWindow", "设置"))
        self.about_action.setText(_translate("MainWindow", "关于"))
        self.official_website_action.setText(_translate("MainWindow", "官网"))
