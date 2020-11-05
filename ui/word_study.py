# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'word_study.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_word_study(object):
    def setupUi(self, word_study):
        word_study.setObjectName("word_study")
        word_study.resize(421, 240)
        self.next_button = QtWidgets.QPushButton(word_study)
        self.next_button.setGeometry(QtCore.QRect(210, 200, 80, 23))
        self.next_button.setObjectName("next_button")
        self.pre_button = QtWidgets.QPushButton(word_study)
        self.pre_button.setGeometry(QtCore.QRect(120, 200, 80, 23))
        self.pre_button.setObjectName("pre_button")
        self.japanese_text_edit = QtWidgets.QPlainTextEdit(word_study)
        self.japanese_text_edit.setGeometry(QtCore.QRect(30, 30, 161, 141))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.japanese_text_edit.setFont(font)
        self.japanese_text_edit.setObjectName("japanese_text_edit")
        self.chinese_text_edit = QtWidgets.QPlainTextEdit(word_study)
        self.chinese_text_edit.setGeometry(QtCore.QRect(230, 30, 161, 141))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.chinese_text_edit.setFont(font)
        self.chinese_text_edit.setObjectName("chinese_text_edit")

        self.retranslateUi(word_study)
        QtCore.QMetaObject.connectSlotsByName(word_study)

    def retranslateUi(self, word_study):
        _translate = QtCore.QCoreApplication.translate
        word_study.setWindowTitle(_translate("word_study", "日文卡牌常见词汇学习"))
        self.next_button.setText(_translate("word_study", "下一个"))
        self.pre_button.setText(_translate("word_study", "前一个"))
