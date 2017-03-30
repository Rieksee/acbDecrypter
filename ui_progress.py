# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progress.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Progress(object):
    def setupUi(self, Progress):
        Progress.setObjectName("Progress")
        Progress.resize(500, 317)
        Progress.setMinimumSize(QtCore.QSize(500, 317))
        Progress.setMaximumSize(QtCore.QSize(500, 317))
        self.gridLayout = QtWidgets.QGridLayout(Progress)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(Progress)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.progress_now = QtWidgets.QProgressBar(Progress)
        self.progress_now.setMinimumSize(QtCore.QSize(0, 30))
        self.progress_now.setProperty("value", 0)
        self.progress_now.setObjectName("progress_now")
        self.verticalLayout_2.addWidget(self.progress_now)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(Progress)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.progress_all = QtWidgets.QProgressBar(Progress)
        self.progress_all.setMinimumSize(QtCore.QSize(0, 30))
        self.progress_all.setProperty("value", 0)
        self.progress_all.setObjectName("progress_all")
        self.verticalLayout_3.addWidget(self.progress_all)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.pushButton = QtWidgets.QPushButton(Progress)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Progress)
        self.pushButton.clicked.connect(Progress.cancel)
        QtCore.QMetaObject.connectSlotsByName(Progress)

    def retranslateUi(self, Progress):
        _translate = QtCore.QCoreApplication.translate
        Progress.setWindowTitle(_translate("Progress", "処理状況"))
        self.label.setText(_translate("Progress", "現在の処理"))
        self.label_2.setText(_translate("Progress", "全体の処理"))
        self.pushButton.setText(_translate("Progress", "中止"))

