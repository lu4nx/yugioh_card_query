# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'count.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_count(object):
    def setupUi(self, count):
        count.setObjectName("count")
        count.resize(312, 221)
        self.count_info_text = QtWidgets.QTextBrowser(count)
        self.count_info_text.setGeometry(QtCore.QRect(10, 10, 291, 201))
        self.count_info_text.setObjectName("count_info_text")

        self.retranslateUi(count)
        QtCore.QMetaObject.connectSlotsByName(count)

    def retranslateUi(self, count):
        _translate = QtCore.QCoreApplication.translate
        count.setWindowTitle(_translate("count", "数据统计"))
